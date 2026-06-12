# CS2 Skin Arbitrage & Price Comparison

?? Advanced arbitrage finder for Counter-Strike 2 skin marketplace

Find profitable trading opportunities by comparing prices across multiple skin marketplaces in real-time.

## Features

### ?? Smart Arbitrage Detection

- **Dynamic Price Analysis:** Automatically finds the best prices across all sources
- **Profit Calculation:** Real-time profit/loss percentage including commissions
- **Multi-Source Data:** Fetches from Skinport, CSFloat, dMarket, SkinBaron, Buff163, and more
- **Error Handling:** Gracefully continues if one source fails

### ?? Advanced Filtering

- ? **Reliability Filter:** 1.0-5.0 star rating range
- ?? **Profit Range:** Filter by profit percentage (-100% to +100%)
- ?? **Price Range:** Set minimum and maximum item prices
- ?? **Product Type:** Case, Capsule, Knife, Gloves, Rifle, Pistol
- ?? **Daily Volume:** Filter by daily sales volume

### ?? Smart Commission Calculation

- Customizable site commissions
- Steam tax (15%) built-in
- Target balance calculations
- Automatic quantity needed calculation
- Support for bidirectional trades (Steam ? Cash / Cash ? Steam)

### ?? Data Visualization

- Profit distribution charts
- Site distribution analysis
- Product type breakdown
- Real-time statistics
- Export to CSV/Excel

## Quick Start

### Windows
```bash
# Just double-click this file:
run.bat
```

### Mac/Linux
```bash
chmod +x run.sh
./run.sh
```

### Manual
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Requirements

- Python 3.8+
- Internet connection
- 2GB RAM minimum
- Modern web browser

## How It Works

1. **Data Collection:** Fetches prices from multiple marketplace APIs
2. **Analysis:** Calculates profit/loss with commissions included
3. **Filtering:** Applies user filters to find best opportunities
4. **Visualization:** Displays results with statistics and charts
5. **Export:** Save results to CSV or Excel

## Data Sources

The application fetches real data from:

| Source | Type | Status |
|--------|------|--------|
| Skinport | API | ? Working |
| CSFloat | API | ? Working |
| dMarket | API | ? Working |
| SkinBaron | API | ? Working |
| Buff163 | API | ? Working |

If a source is unavailable, the app continues with others.

## Configuration

### Commission Rates (Customizable)

By default:
- Skinport: 12%
- CSFloat: 2%
- SkinBaron: 15%
- dMarket: 5%
- Steam: 15% (fixed)

Update these in the "Settings" tab for accurate calculations.

## Usage Examples

### Example 1: Find Best Steam ? Cash Deals
1. Set "Transaction Direction" to "Steam ? Cash"
2. Set "Reliability" to 4.0+ stars
3. Set "Profit Range" to 5% - 20%
4. Click Sort by "Profit (High to Low)"
5. View results and export

### Example 2: Bulk Balance Transfer
1. Set "Target Balance" to $500
2. Select transaction site
3. Sort by "Quantity" needed
4. Export to plan your trades

### Example 3: Find Specific Products
1. Filter "Product Type" to only Knives
2. Set "Price Range" to $100-$500
3. Apply filters and view opportunities

## Tips & Tricks

- ?? **Faster Results:** More specific filters = faster responses
- ?? **Data Caching:** Data is cached for 1 hour (click "Refresh" to update)
- ?? **Volume Matters:** Higher volume items = better liquidity
- ? **Trust Ratings:** Higher ratings = more reliable prices
- ?? **Bidirectional:** Try both Steam ? Cash and Cash ? Steam

## Troubleshooting

### "No data fetched"
- Check internet connection
- Some APIs might be temporarily down
- Try refreshing the data

### "Python not found"
- Install from https://www.python.org/downloads/
- Make sure to add Python to PATH

### "Port already in use"
```bash
streamlit run app.py --server.port 8502
```

### "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

## System Requirements

- **OS:** Windows 7+, macOS 10.12+, or Linux
- **RAM:** 2GB minimum
- **Disk:** 500MB for Python + packages
- **Network:** Internet required

## Performance

- Initial data load: 30-60 seconds
- Subsequent calculations: <1 second
- Export operations: <5 seconds
- Data cache: 1 hour

## Disclaimer

?? **Important:**
- This tool is for educational and analysis purposes only
- Do your own research before trading
- Respect Steam Terms of Service
- Past performance doesn't guarantee future results
- Markets are volatile - check prices before executing trades

## Advanced Usage

### Custom Commission Rates
Use the Settings tab to adjust commission rates for each site based on your account type or region.

### Profit Optimization
- Lower "Reliability" filter to see more opportunities
- Increase "Daily Volume" filter for liquid items
- Focus on high-volume products for better execution

### Batch Operations
- Export results to Excel
- Use formulas to plan large trades
- Compare multiple scenarios

## API Rate Limits

The application includes:
- Random delays between requests (1-3 seconds)
- User-Agent rotation
- Automatic retry logic (3 attempts)
- Graceful error handling

This ensures stable operation without overloading servers.

## File Locations

```
Windows: C:\Users\YourUsername\AppData\Local\streamlit\
Mac:     ~/Library/Application Support/streamlit/
Linux:   ~/.streamlit/
```

## Keyboard Shortcuts

- `R` - Refresh data
- `Ctrl+C` - Stop application
- `F5` - Reload browser

## Supported Browsers

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

## Reporting Issues

Found a bug? Please report it:
1. Describe the issue clearly
2. Include error messages
3. Mention your OS and Python version
4. Steps to reproduce

## Contributing

Contributions are welcome! 
- Report bugs
- Suggest features
- Submit pull requests

## License

This project is provided as-is for educational purposes.

## Credits

Built with:
- [Streamlit](https://streamlit.io/) - Web framework
- [Pandas](https://pandas.pydata.org/) - Data analysis
- [Requests](https://requests.readthedocs.io/) - HTTP client

## Support

Need help?
- Check SETUP.md for detailed instructions
- Review troubleshooting section above
- Open an issue on GitHub

---

**Version:** 1.0.0  
**Python:** 3.8+  
**Last Updated:** 2024  
**Status:** Active Development

Made with ?? for CS2 traders and enthusiasts
