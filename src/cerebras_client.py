"""
Cerebras client for parsing clinical trial PDFs and extracting structured data.
"""

import os
import json
import requests
from typing import Dict, Any, Optional
from pypdf import PdfReader


class CerebrasClient:
    """Client for interacting with Cerebras API for clinical trial data extraction."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Cerebras client with API key."""
        self.api_key = api_key or os.getenv("CEREBRAS_API_KEY")
        if not self.api_key:
            raise ValueError("CEREBRAS_API_KEY not found in environment variables")
        
        # Cerebras API endpoint (this might need adjustment based on actual API)
        self.base_url = "https://api.cerebras.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file."""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def chunk_text(self, text: str, max_chunk_size: int = 4000) -> list[str]:
        """Split text into manageable chunks for API processing."""
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            word_size = len(word) + 1  # +1 for space
            if current_size + word_size > max_chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_size = word_size
            else:
                current_chunk.append(word)
                current_size += word_size
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def extract_clinical_data(self, text_chunk: str) -> Dict[str, Any]:
        """Send text chunk to Cerebras for structured clinical trial data extraction."""
        prompt = f"""
        Extract structured clinical trial information from the following text. 
        Return a JSON object with the following fields:
        - title: Study title
        - participants: Number and demographics of participants
        - study_type: Type of clinical trial (Phase I/II/III, randomized, etc.)
        - endpoints: Primary and secondary endpoints
        - results_summary: Key findings and results
        - methodology: Study design and methodology
        - adverse_events: Safety data and adverse events
        - statistical_analysis: Statistical methods and significance
        
        Text to analyze:
        {text_chunk}
        
        Return only valid JSON without any additional text or formatting.
        """
        
        payload = {
            "model": "llama3.1-8b",  # Using available Cerebras model
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.1,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                # Try to parse JSON from the response
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    # If JSON parsing fails, try to extract data from the text directly
                    return self._extract_data_from_text(text_chunk, content)
            else:
                print(f"⚠️  Cerebras API error: {response.status_code} - {response.text}")
                # Fall back to direct text extraction
                return self._extract_data_from_text(text_chunk, "")
                
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Cerebras API request failed: {str(e)}")
            # Fall back to direct text extraction
            return self._extract_data_from_text(text_chunk, "")
    
    def _extract_data_from_text(self, text_chunk: str, api_content: str = "") -> Dict[str, Any]:
        """Fallback method to extract clinical trial data directly from text when API fails."""
        import re
        
        # Initialize result with fallback values
        result = {
            "title": "Unable to extract title",
            "participants": "Unable to extract participant data", 
            "study_type": "Unable to determine study type",
            "endpoints": "Unable to extract endpoints",
            "results_summary": api_content if api_content else "Unable to extract results",
            "methodology": "Unable to extract methodology",
            "adverse_events": "Unable to extract adverse events",
            "statistical_analysis": "Unable to extract statistical analysis"
        }
        
        # Try to extract title (look for common patterns)
        title_patterns = [
            r"Study Title[:\s]+([^\n]+)",
            r"Title[:\s]+([^\n]+)",
            r"Clinical Trial[:\s]+([^\n]+)",
            r"^([A-Z][^.\n]{10,100})\n",  # First line that looks like a title
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, text_chunk, re.IGNORECASE | re.MULTILINE)
            if match:
                result["title"] = match.group(1).strip()
                break
        
        # Try to extract participant count
        participant_patterns = [
            r"(\d{1,3}(?:,\d{3})*)\s*(?:participants?|patients?|subjects?)",
            r"(?:participants?|patients?|subjects?)[:\s]+(\d{1,3}(?:,\d{3})*)",
            r"n\s*=\s*(\d{1,3}(?:,\d{3})*)",
            r"sample size[:\s]+(\d{1,3}(?:,\d{3})*)",
        ]
        
        for pattern in participant_patterns:
            match = re.search(pattern, text_chunk, re.IGNORECASE)
            if match:
                result["participants"] = f"{match.group(1)} participants"
                break
        
        # Try to extract study type/phase
        phase_patterns = [
            r"(Phase\s+[IVX]+)",
            r"(Randomized\s+[^.\n]*)",
            r"(Double-blind\s+[^.\n]*)",
            r"(Placebo-controlled\s+[^.\n]*)",
            r"(Open-label\s+[^.\n]*)",
            r"(Pilot\s+[^.\n]*)",
        ]
        
        for pattern in phase_patterns:
            match = re.search(pattern, text_chunk, re.IGNORECASE)
            if match:
                result["study_type"] = match.group(1)
                break
        
        # Try to extract endpoints
        endpoint_patterns = [
            r"Primary endpoint[:\s]+([^.\n]+)",
            r"Primary outcome[:\s]+([^.\n]+)",
            r"Secondary endpoint[:\s]+([^.\n]+)",
            r"Secondary outcome[:\s]+([^.\n]+)",
        ]
        
        endpoints = []
        for pattern in endpoint_patterns:
            matches = re.findall(pattern, text_chunk, re.IGNORECASE)
            endpoints.extend(matches)
        
        if endpoints:
            result["endpoints"] = "; ".join(endpoints[:3])  # Limit to first 3
        
        # Try to extract results summary (look for key result indicators)
        result_patterns = [
            r"Results[:\s]+([^.\n]{50,500})",
            r"Conclusion[:\s]+([^.\n]{50,500})",
            r"Findings[:\s]+([^.\n]{50,500})",
            r"Outcome[:\s]+([^.\n]{50,500})",
        ]
        
        for pattern in result_patterns:
            match = re.search(pattern, text_chunk, re.IGNORECASE | re.DOTALL)
            if match:
                result["results_summary"] = match.group(1).strip()[:500]  # Limit length
                break
        
        # Try to extract methodology
        method_patterns = [
            r"Method[:\s]+([^.\n]{50,300})",
            r"Design[:\s]+([^.\n]{50,300})",
            r"Study design[:\s]+([^.\n]{50,300})",
        ]
        
        for pattern in method_patterns:
            match = re.search(pattern, text_chunk, re.IGNORECASE)
            if match:
                result["methodology"] = match.group(1).strip()
                break
        
        # Try to extract adverse events
        ae_patterns = [
            r"Adverse event[:\s]+([^.\n]{30,300})",
            r"Safety[:\s]+([^.\n]{30,300})",
            r"Side effect[:\s]+([^.\n]{30,300})",
        ]
        
        for pattern in ae_patterns:
            match = re.search(pattern, text_chunk, re.IGNORECASE)
            if match:
                result["adverse_events"] = match.group(1).strip()
                break
        
        # Try to extract statistical analysis
        stats_patterns = [
            r"Statistical analysis[:\s]+([^.\n]{30,300})",
            r"p-value[:\s]+([^.\n]{20,200})",
            r"Significance[:\s]+([^.\n]{20,200})",
        ]
        
        for pattern in stats_patterns:
            match = re.search(pattern, text_chunk, re.IGNORECASE)
            if match:
                result["statistical_analysis"] = match.group(1).strip()
                break
        
        return result
    
    def merge_extracted_data(self, data_chunks: list[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge data extracted from multiple chunks into a single coherent summary."""
        if not data_chunks:
            return {}
        
        if len(data_chunks) == 1:
            return data_chunks[0]
        
        # Merge logic - prioritize non-empty values and combine information
        merged = {
            "title": "",
            "participants": "",
            "study_type": "",
            "endpoints": "",
            "results_summary": "",
            "methodology": "",
            "adverse_events": "",
            "statistical_analysis": ""
        }
        
        for chunk_data in data_chunks:
            for key in merged.keys():
                if key in chunk_data and chunk_data[key] and chunk_data[key] != f"Unable to extract {key.replace('_', ' ')}":
                    # Convert to string to ensure we can concatenate
                    chunk_value = str(chunk_data[key])
                    
                    if not merged[key]:
                        merged[key] = chunk_value
                    elif key in ["results_summary", "endpoints", "adverse_events"]:
                        # Combine these fields
                        merged[key] += f"\n\n{chunk_value}"
        
        return merged
    
    def parse_clinical_trial_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Complete pipeline: PDF → text extraction → chunking → Cerebras analysis → structured JSON.
        
        Args:
            pdf_path: Path to the clinical trial PDF file
            
        Returns:
            Dict containing structured clinical trial data
        """
        print(f"📄 Extracting text from PDF: {pdf_path}")
        text = self.extract_text_from_pdf(pdf_path)
        
        print(f"📝 Extracted {len(text)} characters of text")
        
        print("🔄 Chunking text for processing...")
        chunks = self.chunk_text(text)
        print(f"📊 Created {len(chunks)} chunks for analysis")
        
        extracted_data = []
        for i, chunk in enumerate(chunks):
            print(f"🧠 Processing chunk {i+1}/{len(chunks)} with Cerebras...")
            try:
                chunk_data = self.extract_clinical_data(chunk)
                extracted_data.append(chunk_data)
            except Exception as e:
                print(f"⚠️  Error processing chunk {i+1}: {str(e)}")
                continue
        
        print("🔄 Merging extracted data...")
        final_data = self.merge_extracted_data(extracted_data)
        
        print("✅ Clinical trial data extraction completed")
        return final_data


# Example usage and testing function
def test_cerebras_client():
    """Test function for the Cerebras client."""
    try:
        client = CerebrasClient()
        print("✅ Cerebras client initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Error initializing Cerebras client: {str(e)}")
        return False


if __name__ == "__main__":
    test_cerebras_client()
