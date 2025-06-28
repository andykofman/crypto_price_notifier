# Crypto Notifier 🚨

A sophisticated cryptocurrency price monitoring and notification system inspired by **Gilfoyle's Bitcoin Warning** from Silicon Valley. Get real-time alerts when your cryptocurrencies drop below critical thresholds and track their recovery patterns.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Under%20Develoment-brightgreen.svg)]()

## 🌟 Features

### Smart Dual-Alert System
- **🚨 Threshold Alerts**: Immediate notification when a cryptocurrency first drops below your configured threshold
- **📊 Movement Alerts**: Ongoing notifications for price movements after threshold crossing
- **🎵 Distinct Sound Alerts**: Different audio cues for threshold vs. movement alerts
- **🔄 Auto-Reset**: System resets when prices recover above threshold

### Advanced Monitoring Logic
- **Step-based Decrease Alerts**: Notify on every `step`-percent further drop (e.g., 5% increments)
- **Immediate Recovery Alerts**: Instant notification on any price increase
- **Direction Tracking**: Smart detection of price direction changes
- **Multi-Coin Support**: Monitor multiple cryptocurrencies simultaneously

### Professional Features
- **Database Integration**: PostgreSQL and SQLite support with Alembic migrations
- **Scheduled Monitoring**: Background task scheduling with APScheduler
- **Cross-Platform**: Windows and Unix/Linux notification support
- **Comprehensive Testing**: Test suite with pytest
- **Configuration Management**: Environment-based configuration

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- PostgreSQL (optional, SQLite supported for development)

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/andykofman/crypto_price_notifier
cd crypto_price_notifier

# Install using pip
pip install -r requirements.txt

# Or install using pip with pyproject.toml
pip install -e .
```

### Environment Setup

1. Copy the environment template:
```bash
cp env.example .env
```

2. Configure your environment variables:
```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/crypto_notifier

# For development (SQLite)
DATABASE_URL=sqlite:///./crypto_notifier.db

# Application Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
```

## ⚡ Quick Start

### 1. Configure Your Cryptocurrencies

Edit `src/notifier/config.py` to set your monitoring preferences:

```python
def get_coin_config() -> List[CoinConfig]:
    return [ 
        CoinConfig(id="bitcoin", name="Bitcoin", threshold=107600, notify_step=0.05),
        CoinConfig(id="ethereum", name="Ethereum", threshold=1000, notify_step=0.05),
        CoinConfig(id="solana", name="Solana", threshold=100, notify_step=0.05),
        # Add more coins as needed
    ]
```

### 2. Run the Notifier

```bash
# Start monitoring (checks every 60 seconds)
python -m src.notifier.runner
```

### 3. Test Notifications

```bash
# Test the notification sounds
python tests/test_sounds.py
```

## ⚙️ Configuration

### Coin Configuration

Each cryptocurrency is configured with:

- **`id`**: CoinGecko API identifier (e.g., "bitcoin", "ethereum")
- **`name`**: Display name for notifications
- **`threshold`**: Price threshold in USD (triggers initial alert)
- **`notify_step`**: Percentage step for subsequent alerts (e.g., 0.05 = 5%)



## 📖 Usage

### Basic Monitoring

```bash
# Start the notifier
python -m src.notifier.runner
```

The system will:
- Check prices every 60 seconds
- Send threshold alerts when prices drop below configured levels
- Send movement alerts for subsequent price changes
- Play different sounds for different alert types

### Alert Types

#### 🚨 Threshold Alert
- **Trigger**: First time price drops below threshold
- **Sound**: Higher-pitched, urgent beep (Windows) or triple beep (Unix)
- **Duration**: 10-second notification timeout
- **Example**: "🚨 Bitcoin Threshold Alert: Bitcoin has dropped below 107600 -> now 107500.00"

#### 📊 Movement Alert
- **Trigger**: Subsequent price movements after threshold crossing
- **Sound**: Standard notification beep
- **Duration**: 5-second notification timeout
- **Examples**: 
  - "Bitcoin Price Drop: Bitcoin continues dropping -> now 107000.00"
  - "Bitcoin Price Recovery: Bitcoin recovering -> now 107200.00"

### Stopping the Notifier

Press `Ctrl+C` to gracefully stop the monitoring. The system will:
- Shutdown the background scheduler
- Log the stop event
- Clean up resources

## 🔧 API Reference

### Core Classes

#### `CoinConfig`
```python
class CoinConfig(BaseModel):
    id: str          # CoinGecko ID
    name: str        # Display name
    threshold: float # Price threshold
    notify_step: float = 0.05 # Alert step percentage
```

#### `AlertLogic`
```python
class AlertLogic:
    def evaluate_threshold(self, current_price: float, threshold: float) -> bool
    def should_notify(self, current_price: float, threshold: float, step: float) -> bool
```

#### `CoinGeckoFetcher`
```python
class CoinGeckoFetcher:
    def fetch_prices(self, coin_ids: list[str], vs_currency: str) -> dict
```

### Key Functions

#### `notify(title, message, alert_type)`
Send a system notification with appropriate sound.

#### `play_sound(sound_type)`
Play different sounds based on alert type:
- `"threshold"`: Urgent sound for threshold crossing
- `"movement"`: Standard sound for price movements

## 🧪 Testing

### Run All Tests
```bash
pytest tests/
```

### Test Specific Components
```bash
# Test alert logic
pytest tests/test_alert_logic.py

# Test price fetching
pytest tests/test_fetcher.py

# Test notifications
pytest tests/test_notify.py

# Test sounds
python tests/test_sounds.py
```

### Test Coverage
```bash
pytest --cov=src tests/
```

## 🛠️ Development

### Project Structure
```
crypto_notifier/
├── src/
│   └── notifier/
│       ├── __init__.py
│       ├── alert_logic.py    # Core alert logic
│       ├── base.py           # Base classes
│       ├── config.py         # Configuration management
│       ├── fetcher.py        # Price data fetching
│       ├── runner.py         # Main application runner
│       └── storage.py        # Database operations
├── tests/                    # Test suite
├── config.py                 # Application config
├── requirements.txt          # Dependencies
└── pyproject.toml           # Project metadata
```

### Database Migrations

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

### Adding New Features

1. **New Alert Types**: Extend `AlertLogic` class
2. **New Data Sources**: Implement new fetcher classes
3. **New Notification Methods**: Add to `notify()` function
4. **Database Models**: Add to `storage.py` and create migrations

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by **Gilfoyle's Bitcoin Warning** from Silicon Valley
- Built with [CoinGecko API](https://www.coingecko.com/en/api) for cryptocurrency data
- Uses [APScheduler](https://apscheduler.readthedocs.io/) for task scheduling
- Notification system powered by [Plyer](https://plyer.readthedocs.io/)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/andykofman/crypto_price_notifier/issues)
andykofman/crypto-price-notifier/discussions)
- **Email**: ali.a@aucegypt.edu

---

**Disclaimer**: This tool is for educational and personal use. Cryptocurrency investments carry significant risk. Always do your own research and consider consulting with financial advisors before making investment decisions.
