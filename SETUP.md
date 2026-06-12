# SETUP & DEPLOYMENT GUIDE

## CS2 Skin Arbitrage Application

### Quick Start

#### Windows Users:
1. Download the repository
2. Double-click `run.bat`
3. Wait for Python packages to install
4. Browser will open automatically

#### Mac/Linux Users:
1. Download the repository
2. Open Terminal in the project directory
3. Run: `chmod +x run.sh && ./run.sh`
4. Browser will open automatically

---

### Manual Installation

#### Requirements:
- Python 3.8 or higher
- pip (comes with Python)
- Internet connection

#### Step-by-step:

**1. Install Python**
- Download from: https://www.python.org/downloads/
- **IMPORTANT:** Check "Add Python to PATH" during installation
- Verify: Open Command Prompt/Terminal and run `python --version`

**2. Clone/Download Repository**
```bash
git clone https://github.com/yourusername/cs2-arbitrage.git
cd cs2-arbitrage
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Run Application**
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

### Troubleshooting

#### "Python not found"
- Install Python from https://www.python.org/downloads/
- Add Python to PATH
- Restart Command Prompt/Terminal

#### "Module not found"
- Run: `pip install -r requirements.txt --upgrade`

#### "Port 8501 already in use"
- Run: `streamlit run app.py --server.port 8502`

#### "Cannot fetch data from sites"
- Check internet connection
- Some sites may be temporarily down
- Try again later

---

### Features

? Real-time data from multiple sources:
- Skinport
- CSFloat
- dMarket
- SkinBaron
- Buff163

? Advanced filtering:
- Reliability rating
- Profit percentage range
- Price range
- Product type
- Daily volume

? Dynamic calculations:
- Commission rates (customizable)
- Steam tax (15%)
- Target balance calculations
- Quantity needed

? Export data:
- CSV format
- Excel format

? Real-time visualizations:
- Profit distribution
- Site distribution
- Product type distribution

---

### System Requirements

- **OS:** Windows 7+, macOS 10.12+, Linux (Ubuntu, Debian, etc.)
- **RAM:** 2GB minimum
- **Disk Space:** 500MB (for Python + packages)
- **Internet:** Required for data fetching

---

### File Structure

```
cs2-arbitrage/
??? app.py                  # Main Streamlit application
??? config.py               # Configuration constants
??? data_fetcher.py         # Data fetching from multiple sources
??? data_manager.py         # DataFrame operations
??? price_analyzer.py       # Price analysis & arbitrage logic
??? commission_calculator.py # Tax & commission calculations
??? requirements.txt        # Python dependencies
??? run.bat                # Windows launcher
??? run.sh                 # Linux/Mac launcher
??? quick_start.bat        # Quick Windows launcher
??? README.md              # User guide
??? SETUP.md               # This file
??? .gitignore             # Git ignore rules
```

---

### API Sources

The application fetches real data from:

1. **Skinport** - Large marketplace
2. **CSFloat** - Inventory API
3. **dMarket** - Marketplace API
4. **SkinBaron** - German marketplace
5. **Buff163** - Asian marketplace

Data is fetched sequentially with error handling. If one source fails, the app continues with others.

---

### Performance Tips

1. **Cache Data:**
   - Data is cached for 1 hour
   - Use "Refresh Data" to update

2. **Optimize Filters:**
   - More specific filters = faster results
   - Reduce display count if slow

3. **Off-Peak Hours:**
   - Fetch data during off-peak hours
   - Less server load = faster results

---

### Security Notes

- This tool is for personal analysis only
- Respect Steam Terms of Service
- Don't use for automated trading
- Be aware of rate limits on APIs

---

### Updates

To update the application:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
streamlit run app.py
```

---

### Support & Issues

If you encounter issues:

1. Check internet connection
2. Restart the application
3. Clear browser cache
4. Try a different filter configuration
5. Check GitHub issues page

---

### Contact

For questions and support:
- Open an issue on GitHub
- Check existing issues for solutions

---

**Version:** 1.0.0
**Last Updated:** 2024
