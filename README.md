# Neighborhood Analyzer

Real estate neighborhood analysis tool for multiple Florida counties. Try the app here: [https://neighborhood-analyzer.streamlit.app/]

## Usage

1. Launch the application
2. Upload property data file
3. Application automatically:
   - Detects county format
   - Processes data
   - Displays analysis

## Stable Version: v1.0.0

Current stable version supports:
- Multiple county formats (Orange, Seminole)
- Automatic format detection
- Price analysis and visualization
- Square footage calculations
- Property statistics

### Supported File Formats
- Seminole County property data
- Orange County ($ delimited)
- Standard CSV format

### Supported Features
- [x] Multi-county support
- [x] Automatic format detection
- [x] Price trends analysis
- [x] Square footage calculations
- [x] Basic statistics
- [x] Data visualization

## Setup

```bash
# Clone the repository
git clone [your-repo-url]

# Go to stable version
git checkout v1.0.0

# Install requirements
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Usage

1. Launch the application
2. Upload property data file
3. Application automatically:
   - Detects county format
   - Processes data
   - Displays analysis

## File Format Support

### Orange County
- Supports $ delimited files
- Standard CSV format
- Examples: anthemPark.csv, audobonPark.csv, bayLakePreserve.csv

### Seminole County
- Supports hierarchical format
- Example: Sutton Place format

## Development

To work on new features:
```bash
# Create new feature branch
git checkout -b feature/new-feature

# Return to stable version
git checkout v1.0.0
```
