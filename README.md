# AI DDR Assistant

Automated system for generating Detailed Diagnostic Reports (DDR) from building inspection and thermal reports (part of Urbanroof's assignment)

## Overview

This system automates the creation of comprehensive DDRs by:
- Extracting structured data from Inspection and Thermal PDF reports
- Combining and deduplicating findings
- Detecting conflicts between observations
- Identifying missing information
- Generating client-friendly diagnostic reports

## Features

- **Multi-source Analysis**: Processes both inspection and thermal reports
- **Conflict Detection**: Identifies contradictions between data sources
- **Missing Data Detection**: Explicitly highlights unavailable information
- **Structured Output**: Generates organized DDR with:
  - Property Issue Summary
  - Area-wise Observations
  - Probable Root Cause
  - Severity Assessment (with reasoning)
  - Recommended Actions
  - Additional Notes
  - Missing/Unclear Information

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Prepare Input Files

Place your PDF reports in `data/raw/`:
- `data/raw/inspection.pdf` - Inspection report
- `data/raw/thermal.pdf` - Thermal report

## Usage

### Development Mode (Mock LLM)

For testing without API calls, set `USE_MOCK = True` in `app/config.py`:

```python
USE_MOCK = True
```

Then run:

```bash
python -m app.main
```

### Production Mode (Real LLM)

For actual Gemini API calls, set `USE_MOCK = False` in `app/config.py`:

```python
USE_MOCK = False
```

Then run:

```bash
python -m app.main
```

## Output

Generated DDR will be saved to:
```
data/outputs/generated_ddr.md
```

## Project Structure

```
ai_ddr_assistant/
├── app/
│   ├── config.py                    # Configuration settings
│   ├── main.py                      # Main pipeline orchestrator
│   ├── extraction/
│   │   ├── llm_client.py           # Gemini API wrapper
│   │   ├── inspection_extractor.py # Inspection data extraction
│   │   └── thermal_extractor.py    # Thermal data extraction
│   ├── processing/
│   │   ├── pdf_parser.py           # PDF text extraction
│   │   ├── text_cleaner.py         # Text preprocessing
│   │   └── section_segmenter.py    # Section extraction
│   ├── intelligence/
│   │   ├── data_normalizer.py      # Data normalization
│   │   ├── deduplicator.py         # Duplicate removal
│   │   ├── area_linker.py          # Area cross-referencing
│   │   ├── conflict_detector.py    # Conflict identification
│   │   └── missing_detector.py     # Missing data detection
│   ├── diagnostics/
│   │   ├── root_cause_mapper.py    # Root cause analysis
│   │   ├── severity_engine.py      # Severity assessment
│   │   └── recommendation_engine.py # Action recommendations
│   └── reporting/
│       ├── ddr_builder.py          # DDR generation
│       └── markdown_renderer.py     # Markdown formatting
├── data/
│   ├── raw/                        # Input PDFs
│   └── outputs/                    # Generated reports
├── tests/                          # Unit tests
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Configuration

Edit `app/config.py` to customize:

- **Model Selection**: Choose Gemini model variant
- **Temperature**: Control randomness (extraction vs generation)
- **Max Tokens**: Set output length limits
- **Mock Mode**: Toggle between mock and real API calls

## Key Design Principles

1. **Factual Accuracy**: Never invents facts; only uses provided data
2. **Explicit Conflicts**: Clearly states contradictions when found
3. **Missing Data Transparency**: Explicitly marks unavailable information
4. **Client-Friendly**: Uses simple language, avoids unnecessary jargon
5. **Structured Processing**: Multi-stage pipeline ensures quality

## Troubleshooting

### API Quota Exceeded
If you see quota errors, either:
- Wait for quota reset
- Upgrade to paid tier
- Use mock mode for development

### PDF Parsing Issues
Ensure PDFs are:
- Text-based (not scanned images)
- Properly formatted
- Not password-protected

### Import Errors
Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

## License

MIT License - See LICENSE file for details
