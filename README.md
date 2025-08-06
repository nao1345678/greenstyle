# Brand Detection System

A comprehensive brand detection system that analyzes web pages to identify commercial brands using multiple detection methods including text analysis, link extraction, and image attribute scanning.

## Overview

This project provides a complete solution for detecting brands on e-commerce websites and other commercial pages. It includes both Python-based scraping tools and JavaScript implementations for browser extensions and client-side detection.

## Core Components

### Python Modules

- **brand_scraper.py**: Core brand detection scraper with configurable delays and error handling
- **advanced_brand_scraper.py**: Enhanced scraper with sophisticated detection algorithms
- **test_brands.py**: Comprehensive test suite for validation and debugging
- **example_usage.py**: Practical usage examples and integration patterns

### JavaScript Modules

- **brand_detection_engine.js**: Client-side brand detection engine
- **brand_detector_extension.ts**: TypeScript implementation for browser extensions
- **simple_brand_detector.js**: Lightweight detection module
- **learning_brand_detector.js**: Machine learning enhanced detector

### Data Files

- **brands_database.csv**: Primary brand database
- **brands_database_fixed.csv**: Corrected and enhanced brand database
- **requirements.txt**: Python dependencies

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ETH.IA
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Brand Detection

Analyze a single URL for brand presence:

```bash
python brand_scraper.py https://example.com
```

### Advanced Configuration

Use the advanced scraper with custom settings:

```bash
python advanced_brand_scraper.py https://example.com --delay 2.0 --verbose
```

### Testing

Run the comprehensive test suite:

```bash
python test_brands.py
```

### JavaScript Integration

Include the brand detection engine in web applications:

```html
<script src="brand_detection_engine.js"></script>
<script>
    const detector = new BrandDetector();
    detector.analyzePage();
</script>
```

## How It Works

### Detection Methods

1. **Text Analysis**: Scans page content for brand mentions using pattern matching
2. **Link Analysis**: Extracts brands from URLs and link text
3. **Image Analysis**: Identifies brands in image alt attributes and titles
4. **Attribute Scanning**: Searches data attributes for brand information

### Brand Database

The system maintains a comprehensive database of commercial brands across multiple categories:

- Fashion and Apparel
- Electronics and Technology
- Automotive
- Cosmetics and Beauty
- Luxury Goods
- Consumer Electronics

### Processing Pipeline

1. **URL Validation**: Ensures the target URL is accessible
2. **Content Extraction**: Retrieves HTML content with proper encoding
3. **Parsing**: Uses BeautifulSoup for structured HTML parsing
4. **Brand Matching**: Applies multiple detection algorithms
5. **Result Compilation**: Aggregates findings from all sources
6. **Output Generation**: Formats results for analysis

## Configuration

### Scraper Settings

- **Delay**: Configurable delays between requests (default: 1.0s)
- **Timeout**: HTTP request timeout settings
- **User-Agent**: Customizable browser identification
- **Retry Logic**: Automatic retry for failed requests

### Brand Detection Parameters

- **Case Sensitivity**: Configurable case matching
- **Fuzzy Matching**: Approximate string matching support
- **Minimum Length**: Filter for brand name length
- **Custom Databases**: Support for external brand lists

## Output Format

Results are provided in structured JSON format:

```json
{
  "url": "https://example.com",
  "total_brands_found": 5,
  "brands": ["nike", "adidas", "apple", "samsung", "sony"],
  "brands_in_text": ["nike", "adidas"],
  "brands_in_links": ["apple", "samsung"],
  "brands_in_images": ["sony"],
  "text_length": 15420,
  "processing_time": 2.34
}
```

## Browser Extension

The TypeScript extension provides real-time brand detection:

- **Content Script**: Analyzes page content as it loads
- **Background Service**: Manages brand database updates
- **Popup Interface**: User-friendly results display
- **Settings Panel**: Customizable detection parameters

## Testing and Validation

### Test Coverage

- **Basic Functionality**: Core detection algorithms
- **Error Handling**: Network failures and invalid URLs
- **Custom Brands**: User-defined brand lists
- **Performance**: Processing time and memory usage
- **Edge Cases**: Special characters and encoding issues

### Validation Methods

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow validation
- **Performance Tests**: Load and stress testing
- **Browser Tests**: Extension functionality verification

## Performance Considerations

### Optimization Strategies

- **Caching**: Result caching for repeated requests
- **Parallel Processing**: Multi-threaded analysis where appropriate
- **Memory Management**: Efficient data structures and cleanup
- **Network Optimization**: Connection pooling and reuse

### Resource Usage

- **CPU**: Minimal processing overhead
- **Memory**: Efficient string handling and data structures
- **Network**: Respectful request patterns with delays
- **Storage**: Compact result formats

## Security and Ethics

### Responsible Usage

- **Rate Limiting**: Built-in delays to prevent server overload
- **User-Agent**: Proper browser identification
- **Error Handling**: Graceful failure without server impact
- **Data Privacy**: No personal information collection

### Legal Compliance

- **robots.txt**: Respect for site crawling policies
- **Terms of Service**: Compliance with website usage terms
- **Data Protection**: No sensitive data collection or storage
- **Educational Purpose**: Intended for research and learning

## Troubleshooting

### Common Issues

**Connection Errors**
- Verify internet connectivity
- Check URL accessibility
- Increase delay settings
- Verify firewall settings

**No Brands Detected**
- Confirm URL is correct
- Try product or category pages
- Extend brand database
- Check for JavaScript-rendered content

**Module Import Errors**
- Install all dependencies: `pip install -r requirements.txt`
- Verify Python version compatibility
- Check file permissions
- Validate import paths

### Debug Mode

Enable verbose output for detailed analysis:

```bash
python brand_scraper.py https://example.com --verbose
```

## Development

### Project Structure

```
ETH.IA/
├── brand_scraper.py              # Core detection module
├── advanced_brand_scraper.py     # Enhanced detection
├── test_brands.py               # Test suite
├── example_usage.py             # Usage examples
├── brand_detection_engine.js    # JavaScript engine
├── brand_detector_extension.ts  # Browser extension
├── brands_database.csv          # Brand database
├── requirements.txt             # Python dependencies
└── README.md                   # This file
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request
5. Ensure all tests pass

### Code Standards

- **Python**: PEP 8 compliance
- **JavaScript**: ESLint configuration
- **TypeScript**: Strict type checking
- **Documentation**: Comprehensive docstrings
- **Testing**: Minimum 80% coverage

## License

This project is provided for educational and research purposes. Users are responsible for complying with website terms of service and applicable laws when using this software.

## Support

For issues, questions, or contributions:

1. Check existing documentation
2. Review test cases for examples
3. Examine error logs for debugging
4. Submit detailed issue reports

## Version History

- **v1.0.0**: Initial release with core functionality
- **v1.1.0**: Added advanced scraper and browser extension
- **v1.2.0**: Enhanced brand database and performance optimizations
- **v1.3.0**: Comprehensive test suite and documentation updates 