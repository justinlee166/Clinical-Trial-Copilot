# Data Directory

Place your clinical trial PDF files in this directory for analysis.

## Usage Examples

```bash
# Analyze a single PDF
python main.py data/clinical_trial_report.pdf

# Analyze with custom output directory
python main.py data/trial_phase2.pdf --output results/phase2/

# Enable verbose logging
python main.py data/oncology_study.pdf --verbose
```

## Supported File Types

- PDF files (`.pdf`) containing clinical trial reports
- Files should contain structured clinical trial data including:
  - Study title and objectives
  - Participant demographics
  - Study methodology
  - Results and outcomes
  - Safety data
  - Statistical analysis

## File Naming Suggestions

For better organization, consider naming your files descriptively:
- `phase2_oncology_drug_x_2024.pdf`
- `cardiovascular_trial_interim_analysis.pdf`
- `diabetes_medication_safety_study.pdf`
