# Energy Usage Analysis Agent

This is a local implementation of an energy usage analysis agent that helps you analyze your electricity bills and usage patterns.

## Setup

1. **Install Python 3.8+** if you haven't already.

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables**:
   - Create or edit the `.env` file in the project root
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

4. **Prepare your data files**:
   - Place your interval data CSV files in the `data/interval_data/` directory
   - Place your billing data CSV file in the `data/billing_data/` directory

## Running the Application

To start the interactive chat interface:

```bash
python energy_agent.py
```

## Example Queries

- "How much electricity did I use last month?"
- "What was my total bill for Q1 2023?"
- "Show me a summary of my energy usage"
- "How does my current usage compare to last month?"

## Data Format

### Billing Data
Your billing data CSV should have the following columns:
- START DATE (MM/DD/YY)
- END DATE (MM/DD/YY)
- USAGE (kWh)
- COST (with $ sign, e.g., $123.45)

### Interval Data
Your interval data CSVs should have the following columns:
- DATE (MM/DD/YY)
- START TIME (HH:MM)
- END TIME (HH:MM)
- USAGE (kWh)
- COST (with $ sign, e.g., $1.23)

## Notes

- The application uses GPT-4 for natural language understanding
- All data is processed locally
- The application maintains conversation history during the session
