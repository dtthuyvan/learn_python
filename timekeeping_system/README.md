# ⏰ Timekeeping System

A modern, AI-powered employee time tracking and management system built with FastAPI, MongoDB, and Google Gemini AI. This system provides comprehensive employee management, time tracking, and intelligent analytics through natural language interaction.

## 🚀 Features

### 👥 Employee Management
- **CRUD Operations**: Add, view, edit, and delete employees
- **Bulk Import**: Upload employee data via CSV files
- **Employee Profiles**: Store name, date of birth, team, and gender information
- **Smart Analytics**: AI-powered gender distribution analysis

### 🕒 Time Tracking
- **Check-in/Check-out**: Record employee work hours
- **CSV Import**: Bulk upload timesheet data
- **Working Hours Calculation**: Automatic duration calculation
- **Flexible Time Formats**: Support for 12-hour and 24-hour time formats

### 🤖 AI-Powered Analytics
- **Natural Language Queries**: Ask questions in plain English
- **Intelligent Reporting**: Automated analysis of attendance patterns
- **Smart Insights**: Identify employees with insufficient working hours
- **Full Attendance Analysis**: Track complete attendance records
- **Real-time Chat Interface**: Interactive AI communication

### 📊 Advanced Reporting
- **Insufficient Working Hours Report**: Identify employees not meeting minimum requirements
- **Full-time Work Analysis**: Find employees working complete shifts
- **Attendance Patterns**: Comprehensive attendance analytics
- **Gender Distribution Reports**: Demographic analysis

## 🏗️ Architecture

### Backend Stack
- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database for flexible data storage
- **Uvicorn**: Lightning-fast ASGI server
- **Pydantic**: Data validation and serialization

### AI & Machine Learning
- **Google Gemini 2.5 Flash**: Advanced language model
- **Google ADK**: Agent Development Kit for intelligent agents
- **RAG System**: Retrieval-Augmented Generation for context-aware responses
- **Vector Search**: Efficient document similarity search

### Frontend & UI
- **Jinja2 Templates**: Server-side templating engine
- **Tailwind CSS**: Utility-first CSS framework
- **Responsive Design**: Mobile-friendly interface
- **Real-time Chat**: Interactive AI communication interface

## 📁 Project Structure

```
timekeeping_system/
├── app/                    # Main FastAPI application
│   ├── core/              # Database configuration
│   ├── models/            # Data models & serialization
│   ├── routes/            # API endpoints
│   ├── services/          # Business logic & AI services
│   ├── templates/         # HTML templates
│   └── static/            # CSV data files
├── a2a/                   # AI Agent system
│   ├── agents/            # Specialized AI agents
│   ├── host_agent/        # Main agent orchestrator
│   └── services/          # AI-related services
└── requirements.txt        # Python dependencies
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- MongoDB instance
- Google Gemini API key

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd timekeeping_system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   MONGO_CONNECTION_STRING=mongodb://localhost:27017
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

4. **Database Setup**
   - Ensure MongoDB is running
   - The system will automatically create required collections

## 🚀 Running the Application

### Main Application (Port 8000)
```bash
cd app
python main.py
```
Or with uvicorn:
```bash
cd app
uvicorn main:app --reload --port 8000
```

### AI Agent System (Port 10000)
```bash
cd a2a/host_agent
python agent.py
```

### Access the Application
- **Main App**: http://127.0.0.1:8000
- **AI Agent API**: http://127.0.0.1:10000

## 📖 Usage Guide

### Employee Management
1. Navigate to `/employees` to view all employees
2. Use `/employees/add` to add new employees
3. Upload CSV files via `/employees/upload`
4. Generate reports using the AI-powered analytics

### Time Tracking
1. Access `/timekeeping` to view all records
2. Add new entries via `/timekeeping/add`
3. Bulk import data using `/timekeeping/upload`
4. Generate intelligent reports through AI analysis

### AI Interaction
1. Use the chat interface on the main page
2. Ask questions in natural language:
   - "Find employees with insufficient working hours"
   - "Show gender distribution report"
   - "List employees with full attendance"
   - "Analyze working patterns for this week"

## 🔌 API Endpoints

### Employee Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/employees` | List all employees |
| GET | `/employees/add` | Show add employee form |
| POST | `/employees/add` | Create new employee |
| DELETE | `/employees/{id}` | Delete employee |
| POST | `/employees/upload` | Upload CSV file |
| GET | `/employees/gender-report` | Generate gender analysis |

### Timekeeping Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/timekeeping` | List all time records |
| GET | `/timekeeping/add` | Show add timekeeping form |
| POST | `/timekeeping/add` | Create new time record |
| POST | `/timekeeping/upload` | Upload CSV file |
| GET | `/timekeeping/insufficient-report` | Insufficient hours report |
| GET | `/timekeeping/full-hour-report` | Full-time work analysis |
| GET | `/timekeeping/full-attendance-report` | Complete attendance report |

### AI Agent API
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/prompt` | Send natural language query to AI |

## 🤖 AI Agents

### Available Agents
1. **Gender Count Agent**: Analyzes employee gender distribution
2. **Full Attendance Agent**: Tracks complete attendance records
3. **Insufficient Working Time Agent**: Identifies employees not meeting requirements
4. **Employee RAG Agent**: Retrieves employee information using RAG
5. **Timesheet RAG Agent**: Analyzes timesheet data with context

### Agent Capabilities
- **Intent Classification**: Automatically routes queries to appropriate agents
- **Dynamic Routing**: Intelligent query distribution
- **Session Management**: Maintains conversation context
- **Natural Language Processing**: Understands human-like queries

## 📊 Data Models

### Employee Schema
```json
{
  "id": "ObjectId",
  "name": "string",
  "dob": "date",
  "team": "string",
  "gender": "string"
}
```

### Timekeeping Schema
```json
{
  "id": "ObjectId",
  "name": "string",
  "date": "date",
  "checkin": "time (12h format)",
  "checkout": "time (12h format)"
}
```

## 🔧 Configuration

### Environment Variables
- `MONGO_CONNECTION_STRING`: MongoDB connection string
- `GOOGLE_API_KEY`: Google Gemini API key

### Database Collections
- `employee`: Employee information
- `timekeeping_tracking`: Time tracking records
- `employee_train`: Training data for AI models
- `timesheet_train`: Timesheet training data

## 🧪 Testing

### Manual Testing
1. Start both applications (main app + AI agent)
2. Navigate through all routes
3. Test CRUD operations
4. Verify AI agent responses
5. Test CSV upload functionality

### API Testing
Use tools like Postman or curl to test endpoints:
```bash
# Test AI agent
curl --location 'http://127.0.0.1:10000/prompt' \
--header 'Content-Type: application/json' \
--data '{
    "prompt": "Find employees with full attendance"
}'
```

## 🚀 Deployment

### Production Considerations
1. **Environment Variables**: Secure API keys and connection strings
2. **Database Security**: Implement proper MongoDB authentication
3. **HTTPS**: Use SSL/TLS for production
4. **Load Balancing**: Consider multiple instances for high availability
5. **Monitoring**: Implement logging and monitoring solutions

### Docker Support
```dockerfile
# Example Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code examples

## 🔮 Future Enhancements

- [ ] Real-time notifications
- [ ] Mobile application
- [ ] Advanced analytics dashboard
- [ ] Integration with HR systems
- [ ] Machine learning model training
- [ ] Multi-language support
- [ ] Advanced reporting features
- [ ] API rate limiting
- [ ] User authentication system
- [ ] Audit logging

---

**Built with ❤️ using FastAPI, MongoDB, and Google Gemini AI**

*Last updated: December 2024*
