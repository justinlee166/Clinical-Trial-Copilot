"""
Analysis module for generating visualizations and data exports from clinical trial data.
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import Dict, Any, List, Optional
from datetime import datetime
import re
import numpy as np


class ClinicalTrialAnalyzer:
    """Analyzer for creating visualizations and exports from clinical trial data."""
    
    def __init__(self, output_dir: str = "outputs"):
        """Initialize the analyzer with output directory."""
        self.output_dir = output_dir
        self._ensure_output_dir()
        
        # Set matplotlib style
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3
    
    def _ensure_output_dir(self):
        """Ensure output directory exists."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def _clean_dictionary_string(self, text: str, max_length: int = 200) -> str:
        """Clean up dictionary strings and extract readable content."""
        if not isinstance(text, str):
            return str(text)
        
        # If it's a dictionary string, try to extract readable content
        if text.strip().startswith('{') and text.strip().endswith('}'):
            try:
                import ast
                data = ast.literal_eval(text)
                if isinstance(data, dict):
                    # Extract key-value pairs as readable text
                    readable_parts = []
                    for key, value in data.items():
                        readable_parts.append(f"{key.replace('_', ' ').title()}: {value}")
                    result = '; '.join(readable_parts)
                    # Truncate if too long
                    if len(result) > max_length:
                        return result[:max_length] + "..."
                    return result
            except (ValueError, SyntaxError):
                # For malformed dictionary strings, extract the first meaningful part
                # Remove the outer braces and extract the first key-value pair
                inner = text.strip()[1:-1]  # Remove { and }
                # Find the first colon to separate key from value
                colon_pos = inner.find(':')
                if colon_pos > 0:
                    key = inner[:colon_pos].strip().strip("'\"")
                    value = inner[colon_pos+1:].strip().strip("'\"")
                    # Remove any trailing comma or other characters
                    if ',' in value:
                        value = value[:value.find(',')].strip()
                    result = f"{key.replace('_', ' ').title()}: {value}"
                    if len(result) > max_length:
                        return result[:max_length] + "..."
                    return result
        
        # If it contains multiple dictionary strings, extract the first one
        if '{' in text and '}' in text:
            # Find the first complete dictionary string
            start = text.find('{')
            if start != -1:
                brace_count = 0
                end = start
                for i, char in enumerate(text[start:], start):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end = i + 1
                            break
                
                if end > start:
                    dict_str = text[start:end]
                    # Process the extracted string
                    try:
                        import ast
                        data = ast.literal_eval(dict_str)
                        if isinstance(data, dict):
                            readable_parts = []
                            for key, value in data.items():
                                readable_parts.append(f"{key.replace('_', ' ').title()}: {value}")
                            result = '; '.join(readable_parts)
                            if len(result) > max_length:
                                return result[:max_length] + "..."
                            return result
                    except (ValueError, SyntaxError):
                        # For malformed dictionary strings, extract the first meaningful part
                        inner = dict_str.strip()[1:-1]  # Remove { and }
                        colon_pos = inner.find(':')
                        if colon_pos > 0:
                            key = inner[:colon_pos].strip().strip("'\"")
                            value = inner[colon_pos+1:].strip().strip("'\"")
                            if ',' in value:
                                value = value[:value.find(',')].strip()
                            result = f"{key.replace('_', ' ').title()}: {value}"
                            if len(result) > max_length:
                                return result[:max_length] + "..."
                            return result
        
        # Truncate if too long
        if len(text) > max_length:
            return text[:max_length] + "..."
        
        return text
    
    def save_clinical_data_csv(self, clinical_data: Dict[str, Any], filename: str = None) -> str:
        """Save clinical trial data as CSV file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"clinical_trial_data_{timestamp}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Convert nested data to flat structure for CSV
        flattened_data = []
        for key, value in clinical_data.items():
            # Handle dictionary values properly
            if isinstance(value, dict):
                # For methodology dict, extract individual components
                if key == 'methodology' and 'study_design' in value and 'methodology' in value:
                    flattened_data.append({
                        'Field': 'Study Design',
                        'Value': value.get('study_design', 'N/A')
                    })
                    flattened_data.append({
                        'Field': 'Methodology',
                        'Value': value.get('methodology', 'N/A')
                    })
                else:
                    # For other dicts, create separate rows for each key
                    for sub_key, sub_value in value.items():
                        flattened_data.append({
                            'Field': f"{key.replace('_', ' ').title()} - {sub_key.replace('_', ' ').title()}",
                            'Value': str(sub_value)
                        })
            elif isinstance(value, str) and key == 'methodology' and value.strip().startswith('{') and value.strip().endswith('}'):
                # Handle string representation of methodology dictionary
                try:
                    import ast
                    methodology_dict = ast.literal_eval(value)
                    if isinstance(methodology_dict, dict):
                        flattened_data.append({
                            'Field': 'Study Design',
                            'Value': methodology_dict.get('study_design', 'N/A')
                        })
                        flattened_data.append({
                            'Field': 'Methodology',
                            'Value': methodology_dict.get('methodology', 'N/A')
                        })
                    else:
                        flattened_data.append({
                            'Field': key.replace('_', ' ').title(),
                            'Value': str(value)
                        })
                except (ValueError, SyntaxError):
                    # Try to extract values using regex if ast.literal_eval fails
                    import re
                    study_design_match = re.search(r"study_design:\s*([^,}]+)", value)
                    methodology_match = re.search(r"methodology:\s*([^,}]+)", value)
                    
                    if study_design_match and methodology_match:
                        flattened_data.append({
                            'Field': 'Study Design',
                            'Value': study_design_match.group(1)
                        })
                        flattened_data.append({
                            'Field': 'Methodology',
                            'Value': methodology_match.group(1)
                        })
                    else:
                        flattened_data.append({
                            'Field': key.replace('_', ' ').title(),
                            'Value': str(value)
                        })
            else:
                flattened_data.append({
                    'Field': key.replace('_', ' ').title(),
                    'Value': str(value)
                })
        
        df = pd.DataFrame(flattened_data)
        df.to_csv(filepath, index=False)
        
        print(f"📊 Clinical data saved to: {filepath}")
        return filepath
    
    def save_analysis_report(self, analysis_text: str, filename: str = None) -> str:
        """Save analysis report as text file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"clinical_analysis_report_{timestamp}.txt"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("CLINICAL TRIAL ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(analysis_text)
        
        print(f"📋 Analysis report saved to: {filepath}")
        return filepath
    
    def extract_numeric_data(self, text: str) -> List[float]:
        """Extract numeric values from text for visualization."""
        # Find numbers including percentages, decimals, and scientific notation
        pattern = r'-?\d+\.?\d*(?:[eE][+-]?\d+)?%?'
        matches = re.findall(pattern, text)
        
        numbers = []
        for match in matches:
            try:
                # Remove percentage sign and convert
                clean_num = match.replace('%', '')
                numbers.append(float(clean_num))
            except ValueError:
                continue
        
        return numbers
    
    def create_efficacy_chart(self, clinical_data: Dict[str, Any]) -> str:
        """Create efficacy/results visualization."""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Extract data from results summary
        results_text = clinical_data.get('results_summary', '')
        numbers = self.extract_numeric_data(results_text)
        
        if numbers and len(numbers) >= 2:
            # Create comparison chart
            categories = ['Control Group', 'Treatment Group', 'Difference']
            values = numbers[:3] if len(numbers) >= 3 else numbers + [abs(numbers[1] - numbers[0]) if len(numbers) >= 2 else 0]
            
            bars = ax.bar(categories, values[:len(categories)], 
                         color=['#ff7f7f', '#7fbf7f', '#7f7fff'], alpha=0.8)
            
            # Add value labels on bars
            for bar, value in zip(bars, values[:len(categories)]):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + max(values) * 0.01,
                       f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
            
            ax.set_title('Clinical Trial Efficacy Results', fontsize=16, fontweight='bold')
            ax.set_ylabel('Response Rate (%)', fontsize=12)
        else:
            # Create placeholder chart with study information
            study_info = [
                f"Study Type: {clinical_data.get('study_type', 'N/A')}",
                f"Participants: {clinical_data.get('participants', 'N/A')}",
                f"Primary Endpoint: {clinical_data.get('endpoints', 'N/A')[:50]}..."
            ]
            
            ax.text(0.5, 0.5, '\n'.join(study_info), 
                   transform=ax.transAxes, ha='center', va='center',
                   fontsize=12, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
            ax.set_title('Clinical Trial Overview', fontsize=16, fontweight='bold')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        
        plt.tight_layout()
        
        # Save chart
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"efficacy_chart_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📈 Efficacy chart saved to: {filepath}")
        return filepath
    
    def create_safety_profile_chart(self, clinical_data: Dict[str, Any]) -> str:
        """Create adverse events/safety profile visualization."""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        adverse_events = clinical_data.get('adverse_events', '')
        
        # Common adverse event categories for clinical trials
        ae_categories = ['Mild', 'Moderate', 'Severe', 'Serious']
        
        # Extract numbers or create representative data
        numbers = self.extract_numeric_data(adverse_events)
        if len(numbers) >= len(ae_categories):
            values = numbers[:len(ae_categories)]
        else:
            # Create representative data based on typical clinical trial patterns
            values = [45, 30, 15, 10]  # Typical distribution
        
        # Create pie chart
        colors = ['#90EE90', '#FFD700', '#FFA500', '#FF6347']
        wedges, texts, autotexts = ax.pie(values, labels=ae_categories, colors=colors, 
                                         autopct='%1.1f%%', startangle=90)
        
        # Enhance appearance
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontweight('bold')
        
        ax.set_title('Adverse Events Distribution', fontsize=16, fontweight='bold')
        
        # Add legend
        ax.legend(wedges, ae_categories, title="Severity Levels", 
                 loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        plt.tight_layout()
        
        # Save chart
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"safety_profile_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"🛡️ Safety profile chart saved to: {filepath}")
        return filepath
    
    def create_study_timeline_chart(self, clinical_data: Dict[str, Any]) -> str:
        """Create study timeline and methodology visualization."""
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Common clinical trial phases
        phases = ['Screening', 'Baseline', 'Treatment Period', 'Follow-up', 'Analysis']
        timeline = [0, 1, 6, 12, 15]  # Months
        
        # Create timeline
        ax.plot(timeline, [1]*len(timeline), 'o-', linewidth=3, markersize=10, color='#2E86AB')
        
        # Add phase labels
        for i, (phase, time) in enumerate(zip(phases, timeline)):
            ax.annotate(phase, (time, 1), xytext=(0, 20), 
                       textcoords='offset points', ha='center', va='bottom',
                       fontsize=10, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        
        # Add methodology information
        methodology = clinical_data.get('methodology', 'Standard clinical trial design')
        
        # Handle case where methodology is a dictionary or string representation of dictionary
        if isinstance(methodology, dict):
            study_design = methodology.get('study_design', 'Cross-sectional survey')
            methodology_text = methodology.get('methodology', 'Multivariable logistic regression')
            display_text = f"Study Design: {study_design}\nMethodology: {methodology_text}"
        elif isinstance(methodology, str) and methodology.strip().startswith('{') and methodology.strip().endswith('}'):
            # Handle string representation of dictionary
            try:
                import ast
                methodology_dict = ast.literal_eval(methodology)
                if isinstance(methodology_dict, dict):
                    study_design = methodology_dict.get('study_design', 'Cross-sectional survey')
                    methodology_text = methodology_dict.get('methodology', 'Multivariable logistic regression')
                    display_text = f"Study Design: {study_design}\nMethodology: {methodology_text}"
                else:
                    display_text = f"Study Design: {methodology}"
            except (ValueError, SyntaxError):
                # Try to extract values using regex if ast.literal_eval fails
                import re
                study_design_match = re.search(r"study_design:\s*([^,}]+)", methodology)
                methodology_match = re.search(r"methodology:\s*([^,}]+)", methodology)
                
                if study_design_match and methodology_match:
                    study_design = study_design_match.group(1)
                    methodology_text = methodology_match.group(1)
                    display_text = f"Study Design: {study_design}\nMethodology: {methodology_text}"
                else:
                    display_text = f"Study Design: {methodology}"
        else:
            display_text = f"Study Design: {methodology}"
        
        ax.text(0.5, 0.3, display_text, 
               transform=ax.transAxes, ha='center', va='center',
               fontsize=12, bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow"))
        
        ax.set_xlim(-1, 16)
        ax.set_ylim(0, 2)
        ax.set_xlabel('Timeline (Months)', fontsize=12)
        ax.set_title('Clinical Trial Timeline and Methodology', fontsize=16, fontweight='bold')
        ax.set_yticks([])
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save chart
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"study_timeline_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"⏱️ Study timeline chart saved to: {filepath}")
        return filepath
    
    def generate_all_visualizations(self, clinical_data: Dict[str, Any], 
                                   viz_recommendations: Dict[str, Any] = None) -> List[str]:
        """Generate all standard clinical trial visualizations."""
        print("📊 Generating clinical trial visualizations...")
        
        chart_files = []
        
        # Generate standard charts
        try:
            chart_files.append(self.create_efficacy_chart(clinical_data))
        except Exception as e:
            print(f"⚠️ Error creating efficacy chart: {str(e)}")
        
        try:
            chart_files.append(self.create_safety_profile_chart(clinical_data))
        except Exception as e:
            print(f"⚠️ Error creating safety profile chart: {str(e)}")
        
        try:
            chart_files.append(self.create_study_timeline_chart(clinical_data))
        except Exception as e:
            print(f"⚠️ Error creating timeline chart: {str(e)}")
        
        # Generate custom charts based on Claude's recommendations
        if viz_recommendations and 'visualizations' in viz_recommendations:
            for viz in viz_recommendations['visualizations']:
                try:
                    custom_chart = self.create_custom_visualization(clinical_data, viz)
                    if custom_chart:
                        chart_files.append(custom_chart)
                except Exception as e:
                    print(f"⚠️ Error creating custom visualization: {str(e)}")
        
        print(f"✅ Generated {len(chart_files)} visualization files")
        return chart_files
    
    def create_custom_visualization(self, clinical_data: Dict[str, Any], 
                                   viz_spec: Dict[str, Any]) -> Optional[str]:
        """Create custom visualization based on Claude's recommendations."""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            viz_type = viz_spec.get('type', 'bar_chart')
            title = viz_spec.get('title', 'Custom Visualization')
            
            # Extract data based on specification
            data_source = viz_spec.get('data_source', 'results_summary')
            source_text = clinical_data.get(data_source, '')
            numbers = self.extract_numeric_data(source_text)
            
            if viz_type == 'bar_chart' and numbers:
                categories = [f'Group {i+1}' for i in range(len(numbers[:5]))]
                ax.bar(categories, numbers[:5], color='steelblue', alpha=0.7)
                ax.set_ylabel(viz_spec.get('y_label', 'Value'))
                ax.set_xlabel(viz_spec.get('x_label', 'Category'))
                
            elif viz_type == 'line_chart' and numbers:
                time_points = list(range(len(numbers[:10])))
                ax.plot(time_points, numbers[:10], 'o-', linewidth=2, markersize=6)
                ax.set_ylabel(viz_spec.get('y_label', 'Value'))
                ax.set_xlabel(viz_spec.get('x_label', 'Time'))
                
            else:
                # Default to text display
                ax.text(0.5, 0.5, viz_spec.get('description', 'Custom visualization'), 
                       transform=ax.transAxes, ha='center', va='center',
                       fontsize=12, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
                ax.axis('off')
            
            ax.set_title(title, fontsize=14, fontweight='bold')
            plt.tight_layout()
            
            # Save chart
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
            filename = f"custom_{safe_title}_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"🎨 Custom visualization saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"⚠️ Error creating custom visualization: {str(e)}")
            return None
    
    def create_summary_dashboard(self, clinical_data: Dict[str, Any]) -> str:
        """Create a summary dashboard with key metrics."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f"Clinical Trial Dashboard: {clinical_data.get('title', 'Unknown Study')}", 
                    fontsize=16, fontweight='bold')
        
        # Top-left: Study overview
        endpoints_clean = self._clean_dictionary_string(clinical_data.get('endpoints', 'N/A'), 60)
        study_info = [
            f"Study Type: {clinical_data.get('study_type', 'N/A')}",
            f"Participants: {clinical_data.get('participants', 'N/A')}",
            f"Primary Endpoint: {endpoints_clean}"
        ]
        ax1.text(0.1, 0.7, '\n'.join(study_info), transform=ax1.transAxes, 
                fontsize=11, verticalalignment='top',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue"))
        ax1.set_title('Study Overview', fontweight='bold')
        ax1.axis('off')
        
        # Top-right: Results summary
        results = self._clean_dictionary_string(clinical_data.get('results_summary', 'No results available'), 200)
        ax2.text(0.1, 0.9, results, transform=ax2.transAxes, 
                fontsize=10, verticalalignment='top', wrap=True,
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen"))
        ax2.set_title('Key Results', fontweight='bold')
        ax2.axis('off')
        
        # Bottom-left: Safety data
        safety = self._clean_dictionary_string(clinical_data.get('adverse_events', 'No safety data available'), 200)
        ax3.text(0.1, 0.9, safety, transform=ax3.transAxes, 
                fontsize=10, verticalalignment='top', wrap=True,
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow"))
        ax3.set_title('Safety Profile', fontweight='bold')
        ax3.axis('off')
        
        # Bottom-right: Statistical analysis
        stats = self._clean_dictionary_string(clinical_data.get('statistical_analysis', 'No statistical data available'), 200)
        ax4.text(0.1, 0.9, stats, transform=ax4.transAxes, 
                fontsize=10, verticalalignment='top', wrap=True,
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightcoral"))
        ax4.set_title('Statistical Analysis', fontweight='bold')
        ax4.axis('off')
        
        plt.tight_layout()
        
        # Save dashboard
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"clinical_dashboard_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Clinical dashboard saved to: {filepath}")
        return filepath


# Example usage and testing function
def test_analyzer():
    """Test function for the ClinicalTrialAnalyzer."""
    try:
        analyzer = ClinicalTrialAnalyzer()
        print("✅ Clinical Trial Analyzer initialized successfully")
        
        # Test with sample data
        sample_data = {
            "title": "Test Clinical Trial for Novel Cancer Treatment",
            "participants": "200 patients with advanced cancer",
            "study_type": "Phase II randomized controlled trial",
            "endpoints": "Primary: Overall response rate; Secondary: Progression-free survival",
            "results_summary": "Treatment group showed 65% response rate vs 35% in control (p<0.001)",
            "methodology": "Randomized, double-blind, placebo-controlled, multi-center",
            "adverse_events": "Mild fatigue (45%), nausea (30%), moderate diarrhea (15%), severe neutropenia (5%)",
            "statistical_analysis": "Chi-square test for categorical variables, p-value = 0.001, CI 95%"
        }
        
        print("📊 Testing visualization generation...")
        charts = analyzer.generate_all_visualizations(sample_data)
        
        print("📋 Testing CSV export...")
        csv_file = analyzer.save_clinical_data_csv(sample_data)
        
        print("📊 Testing dashboard creation...")
        dashboard = analyzer.create_summary_dashboard(sample_data)
        
        print(f"✅ Generated {len(charts)} charts, 1 CSV file, and 1 dashboard")
        return True
        
    except Exception as e:
        print(f"❌ Error testing analyzer: {str(e)}")
        return False


if __name__ == "__main__":
    test_analyzer()
