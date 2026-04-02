# 🎯 Knowledge Intelligence Analyst

A powerful data intelligence platform that automatically collects, analyzes, and visualizes technical knowledge from multiple online communities using AI-driven topic generation.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Status](https://img.shields.io/badge/status-Active-success)

---

## 🌟 Features

- **🤖 AI-Powered Topic Generation** - Uses LLM (LongCat) to dynamically generate relevant technical topics based on your domain
- **📡 Multi-Platform Scraping** - Collects data from:
  - Reddit
  - Stack Overflow
  - Dev.to
- **📊 Advanced Analytics** - Performs:
  - Sentiment analysis
  - Feature engineering
  - Topic modeling
  - Engagement metrics
- **📈 Visual Dashboards** - Power BI integration for interactive insights
- **🎓 Comprehensive Analysis** - Jupyter notebooks for exploratory data analysis and modeling

---

## 📋 Project Structure

```
Knowledge-Intelligence-Analyst/
├── 📄 README.md                      # Project overview
├── 📋 requirements.txt                # Python dependencies
├── ⚙️  .gitignore                     # Git ignore rules
├── 🔑 .env.example                    # Environment variables template
│
├── 📁 scraping/                       # Web scraping modules
│   ├── main.py                        # Main orchestration script
│   ├── config.py                      # Configuration management
│   ├── reddit_scraper.py              # Reddit data collection
│   ├── stackoverflow_scraper.py        # Stack Overflow data collection
│   ├── devto_scraper.py               # Dev.to data collection
│   ├── utils.py                       # Utility functions
│   └── settings.env                   # Setup configuration
│
├── 📊 data/                           # Data storage
│   ├── raw/                           # Raw collected datasets
│   └── processed/                     # Cleaned and processed data
│
├── 📓 notebooks/                      # Jupyter notebooks
│   └── Analysis_and_Modeling.ipynb    # Data analysis and feature engineering
│
├── 📈 dashboards/                     # Business intelligence dashboards
│   └── dashboard.pbix                 # Power BI dashboard
│
└── 📚 docs/                           # Documentation
    └── Documentation.pdf              # Project documentation
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- API Keys (see [Setup Guide](#-setup))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Dipurajasaha/Knowledge-Intelligence-Analyst.git
   cd Knowledge-Intelligence-Analyst
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Copy example to settings
   cp .env.example scraping/settings.env
   
   # Edit scraping/settings.env with your API keys
   nano scraping/settings.env
   ```

---

## 🔧 Setup

### Environment Variables

Create `scraping/settings.env` with the following:

```env
# Domain of interest for topic generation
DOMAIN=Generative AI & Deep Learning

# Data collection parameters
PLATFORMS=Reddit,StackOverflow,DevTo
MAX_RECORDS_PER_TOPIC=100
TOPIC_COUNT=5

# Reddit API
REDDIT_USER_AGENT=python:projectdatacollector:v1.0

# LLM Configuration (LongCat API)
LONGCAT_API_KEY=your_api_key_here
LONGCAT_MODEL=your_model_name_here

# Data directory
RAW_DATA_DIR=./data/raw
```

### API Keys Required

| Platform | Setup |
|----------|-------|
| **Reddit** | Get User-Agent from Reddit API docs |
| **Stack Overflow** | No authentication needed (uses public API) |
| **Dev.to** | No authentication needed (uses public API) |
| **LongCat LLM** | Register at [LongCat](https://longcat.chat/) |

---

## 📖 Usage

### 1. Collect Data

Run the scraping pipeline:

```bash
cd scraping
python main.py
```

This will:
- Generate topics using LLM based on your domain
- Scrape data from configured platforms
- Save raw data to `data/raw/`

### 2. Process & Analyze Data

Open and run the Jupyter notebook:

```bash
jupyter notebook notebooks/Analysis_and_Modeling.ipynb
```

Features include:
- Data cleaning and preprocessing
- Sentiment analysis
- Feature engineering
- Visualization and insights

### 3. Visualize in Power BI

Open `dashboards/dashboard.pbix` with Microsoft Power BI to:
- Explore engagement metrics
- Compare platforms
- Analyze sentiment trends
- Track topic popularity

---

## 📊 Data Flow

```
LLM Topic Generation
        ↓
Multi-Platform Scraping (Reddit, StackOverflow, Dev.to)
        ↓
Raw Data Storage (data/raw/)
        ↓
Data Cleaning & Feature Engineering (Jupyter Notebook)
        ↓
Processed Data (data/processed/)
        ↓
Power BI Dashboard Visualization
```

---

## 📦 Key Dependencies

```
pandas              # Data manipulation
numpy               # Numerical computing
matplotlib          # Visualization
seaborn             # Statistical visualization
scikit-learn        # Machine learning
nltk                # Natural language processing
requests            # HTTP client
beautifulsoup4      # Web scraping
selenium            # Browser automation
jupyter             # Interactive notebooks
```

Full list: See `requirements.txt`

---

## 🎯 Use Cases

✅ **Market Research** - Understand trending technologies and challenges  
✅ **Competitive Analysis** - Track discussions about your domain  
✅ **Sentiment Analysis** - Gauge community sentiment on topics  
✅ **Knowledge Mining** - Identify key patterns in developer discussions  
✅ **Business Intelligence** - Data-driven decision making  

---

## 📈 Example Outputs

- **Sentiment Metrics**: Positive/Negative/Neutral distribution
- **Engagement Analysis**: Views, comments, upvotes per platform
- **Topic Trends**: Most discussed topics over time
- **Topic Metrics**: Popularity, sentiment by topic
- **Platform Comparison**: Performance comparison across platforms

---

## ⚠️ Rate Limiting & Best Practices

- Reddit: ~60 requests/minute (with User-Agent)
- Stack Overflow: ~10k requests/day (public API)
- Dev.to: Rate-limited per API docs
- Add delays between requests to avoid throttling
- Respect each platform's Terms of Service

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "LongCat API Key missing" | Check `scraping/settings.env` and add your API key |
| "No module named requests" | Run `pip install -r requirements.txt` |
| "Connection timeout" | Check internet connection or increase timeout value |
| "Empty dataset" | Verify API keys and platform availability |

---

## 📝 Documentation

- 📘 See `docs/Documentation.pdf` for detailed project documentation
- 📓 Explore `notebooks/Analysis_and_Modeling.ipynb` for code examples
- 🔑 Check `docs/API_CONFIGURATION.md` for API setup details (if available)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 Author

**Knowledge Intelligence Analyst Team**

- Project Status: Active
- Last Updated: April 2026

---

## 📞 Support

For issues, questions, or suggestions:
- 📧 Open an Issue on GitHub
- 💬 Check existing documentation in `/docs`
- 📖 Review the Analysis notebook for examples

---

## 🙏 Acknowledgments

- Built with industry-standard tools (Pandas, Scikit-learn, NLTK)
- Powered by LongCat LLM for intelligent topic generation
- Community contributions and feedback

---

**⭐ If you find this project useful, please consider giving it a star!**
