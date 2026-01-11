# 🔐 Password Validator Pro

A modern and comprehensive web application for validating and generating secure passwords, built with Flask and Python.

![Password Validator](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-red.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

## ✨ Features

- 🎯 **Real-Time Validation**: Instant feedback as you type
- 📊 **Visual Strength Meter**: Indicates how secure your password is
- ⚡ **Password Generator**: Creates secure, customizable passwords
- 🎨 **Modern Interface**: Design Clean and attractive
- 📱 **Responsive**: Works on desktop, tablet, and mobile
- 🔍 **Advanced Validations**:

- Minimum and maximum length

- Uppercase and lowercase letters

- Numbers and symbols

- Common password detection

- Sequence detection (abc, 123, qwerty)

- Repeated character detection

## 🚀 Demo

![Demo Screenshot](docs/screenshot.png)

## 📋 Requirements

- Python 3.8 or higher
- pip (Python package manager)

## 🔧 Installation

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/password-validator-improved.git
cd password-validator-improved
```

2. **Create Virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open in browser**
```
http://localhost:5000
```

## 📦 Project Structure
```
password-validator-improved/
├── app.py # Main Flask application
├── validator.py # Validation logic
├── templates/
│ └── index.html # HTML frontend
├── static/
│ ├── css/ # Styles (future)
│ └── js/ # JavaScript (future)
├── tests/ # Unit tests
├── docs/ # Documentation
├── requirements.txt # Python dependencies
├── .gitignore # Files ignored by Git
├── LICENSE # MIT License
└── README.md # This file
```

## 🎮 Usage

### Validate Password

1. Enter a password in the text field
2. Observe the real-time strength meter
3. Review the rules met/not met

### Generate Password

1. Adjust the length 1. Select the desired password length using the slider (8-32 characters)
2. Click "Generate Password"
3. Copy the generated password using the "Copy" button

## 🔐 Validation Rules

The application validates the following rules:

- ✅ Minimum 8 characters
- ✅ Maximum 50 characters
- ✅ At least 1 uppercase letter
- ✅ At least 1 lowercase letter
- ✅ At least 1 number
- ✅ At least 1 special symbol
- ✅ No spaces
- ✅ Do not use common passwords
- ✅ No obvious sequences (abc, 123)
- ✅ No repeated characters (aaa, 111)

## 🛠️ Technologies Used

- **Backend**: Python 3, Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Design**: CSS Grid, Flexbox, Gradients

## 📊 API Endpoints

### POST /validate
Validates a password and returns detailed results.

**Request:**
```json
{
"password": "MyPassword123!"

}
```

**Response:**
```json
{
"valid": true,
"results": [...],
"score": 85,
"strength": "Strong"
}
```

### POST /generate
Generates a secure password.


**Request:**
```json
{ 
"length": 16
}
```

**Response:**
```json
{ 
"password": "aB3#xY9@mN2$pQ5&"
}
```

## 🧪 Testing
```bash
# Run tests
python -m pytest tests/

# With coverage
python -m pytest --cov=. tests/
```

## 🚀 Roadmap

- [ ] **Statistics**: Metrics and analytics system
- [ ] **HaveIBeenPwned**: Detection of leaked passwords
- [ ] **Dark Mode**: Toggle dark/light theme
- [ ] **User System**: Login and custom profiles
- [ ] **Docker**: Containerization
- [ ] **Complete Tests**: 100% coverage
- [ ] **CLI**: Command-line tool

## 🤝 Contribute

Contributions are welcome! Please:

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Changelog

### v1.0.0 (2026-01-11)
- ✨ Initial Release
- ✅ Real-time Validation
- ✅ Password Generator
- ✅ Responsive Interface

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Your Name**
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- Email: your-email@example.com

## 🙏 Acknowledgments

- Inspired by [password-validator](https://github.com/tarunbatra/password-validator)
- Flask framework
- Python Community

## 📸 Screenshots

### Main Screen
![Main Screen](docs/screenshots/main.png)

### Validation in Action
![Validation](docs/screenshots/valida

tion.png)

### Password Generator
![Generator](docs/screenshots/generator.png)

---

⭐ If you found this project useful, please give it a star on GitHub!
