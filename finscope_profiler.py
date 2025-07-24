import json
import os
from datetime import datetime
from typing import Dict, List, Tuple
import sys
from colorama import init, Fore, Back, Style
from pyfiglet import figlet_format

# Try to import optional packages for enhanced display
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)  # Initialize colorama
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    # Fallback color class
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Back:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ""

try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False


def print_banner():
    """Display the welcome banner and introduction."""
    BOX_WIDTH = 63
    title_art = figlet_format("FINSCOPE", font="block").rstrip().split("\n")
    subtitle_art = figlet_format("PROFILER", font="block").rstrip().split("\n")
    tagline = "Know Your Investment Personality"

    def box_line(text):
        return (
            Fore.CYAN + Style.BRIGHT + "║" +
            text.center(BOX_WIDTH) +
            "║" + Style.RESET_ALL
        )

    box_top = Fore.CYAN + Style.BRIGHT + "╔" + ("═" * BOX_WIDTH) + "╗"
    box_bottom = Fore.CYAN + Style.BRIGHT + "╚" + ("═" * BOX_WIDTH) + "╝" + Style.RESET_ALL

    print(box_top)
    # Add extra vertical padding for appeal
    print(box_line(""))
    print(box_line(""))
    for line in title_art:
        if line.strip():
            print(box_line(line))
    for line in subtitle_art:
        if line.strip():
            print(box_line(line))
    print(box_line(""))
    print(box_line(""))
    print(box_line(tagline))
    print(box_line(""))
    print(box_line(""))
    print(box_bottom)
    print(f"\n{Fore.YELLOW}Welcome to Finscope Profiler!{Style.RESET_ALL}\n")
    print("This assessment will help you understand your investment risk tolerance and ")
    print("suggest appropriate investment strategies based on your financial behavior,")
    print("goals, and preferences.\n")
    print(f"{Fore.GREEN}What you'll get:{Style.RESET_ALL}")
    print("• Your personal risk profile (Conservative, Balanced, or Aggressive)")
    print("• Tailored investment recommendations")
    print("• Better understanding of your financial personality")
    print("• A saved record of your assessment results\n")
    print(f"{Fore.BLUE}Time required: 5-10 minutes{Style.RESET_ALL}\n")


def get_user_info() -> Dict[str, str]:
    """Collect basic user information."""
    print(f"\n{Fore.MAGENTA}=== USER INFORMATION ==={Style.RESET_ALL}")
    
    name = input(f"{Fore.CYAN}Enter your name: {Style.RESET_ALL}").strip()
    while not name:
        name = input(f"{Fore.RED}Please enter a valid name: {Style.RESET_ALL}").strip()
    
    age = input(f"{Fore.CYAN}Enter your age: {Style.RESET_ALL}").strip()
    while not age.isdigit() or int(age) < 10 or int(age) > 100:
        age = input(f"{Fore.RED}Please enter a valid age (10-100): {Style.RESET_ALL}").strip()
    
    return {
        "name": name,
        "age": age,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def get_questions() -> List[Dict]:
    """Define the assessment questions with scoring weights."""
    questions = [
        {
            "question": "What is your current age group?",
            "options": [
                "Under 18",
                "18-25", 
                "26-35",
                "36-50",
                "Over 50"
            ],
            "scores": [5, 5, 4, 3, 2],
            "category": "demographics"
        },
        {
            "question": "How much of your monthly income do you typically save?",
            "options": [
                "Less than 5%",
                "5-10%",
                "10-20%",
                "20-30%",
                "More than 30%"
            ],
            "scores": [1, 2, 3, 4, 5],
            "category": "savings_habits"
        },
        {
            "question": "What is your primary financial goal?",
            "options": [
                "Building an emergency fund",
                "Saving for a major purchase (car, house)",
                "Long-term wealth building",
                "Generating current income",
                "Aggressive growth and wealth maximization"
            ],
            "scores": [1, 2, 3, 4, 5],
            "category": "financial_goals"
        },
        {
            "question": "How do you react when your investments lose 20% of their value?",
            "options": [
                "Panic and sell immediately",
                "Feel very uncomfortable but hold",
                "Feel concerned but remain calm",
                "See it as a buying opportunity",
                "Excited to invest more at lower prices"
            ],
            "scores": [1, 2, 3, 4, 5],
            "category": "risk_tolerance"
        },
        {
            "question": "What's your investment time horizon?",
            "options": [
                "Less than 1 year",
                "1-3 years",
                "3-7 years",
                "7-15 years",
                "More than 15 years"
            ],
            "scores": [1, 2, 3, 4, 5],
            "category": "time_horizon"
        },
        {
            "question": "How much investment experience do you have?",
            "options": [
                "None - complete beginner",
                "Limited - basic savings accounts",
                "Some - have tried a few investments",
                "Moderate - regularly invest in various assets",
                "Extensive - sophisticated investment strategies"
            ],
            "scores": [1, 2, 3, 4, 5],
            "category": "experience"
        },
        {
            "question": "What percentage of your portfolio would you allocate to high-risk investments?",
            "options": [
                "0% - I avoid all high-risk investments",
                "1-10% - Very small allocation",
                "10-25% - Conservative allocation",
                "25-50% - Moderate allocation",
                "50%+ - Aggressive allocation"
            ],
            "scores": [1, 2, 3, 4, 5],
            "category": "allocation_preference"
        },
        {
            "question": "How important is it to have quick access to your invested money?",
            "options": [
                "Extremely important - need immediate access",
                "Very important - within a few days",
                "Somewhat important - within a month",
                "Not very important - can wait several months",
                "Not important - can lock money away for years"
            ],
            "scores": [1, 2, 3, 4, 5],
            "category": "liquidity_preference"
        },
        {
            "question": "Which statement best describes your attitude toward debt?",
            "options": [
                "I avoid all debt and prefer to pay cash",
                "I only use debt for essentials like housing",
                "I'm comfortable with moderate debt for investments",
                "I actively use debt to leverage investments",
                "I maximize debt to amplify returns"
            ],
            "scores": [1, 2, 3, 4, 5],
            "category": "debt_attitude"
        },
        {
            "question": "If you received 100,000 USD unexpectedly, what would you do?",
            "options": [
                "Put it all in a savings account",
                "Pay off debts and save the rest",
                "Split between savings and safe investments",
                "Invest most of it in a diversified portfolio",
                "Put it all in high-growth investments"
            ],
            "scores": [1, 2, 3, 4, 5],
            "category": "windfall_behavior"
        }
    ]
    return questions


def conduct_assessment(questions: List[Dict]) -> Tuple[int, List[Dict]]:
    """Conduct the risk assessment questionnaire."""
    print(f"\n{Fore.MAGENTA}=== RISK ASSESSMENT QUESTIONNAIRE ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Please answer each question by selecting the number that best describes you.{Style.RESET_ALL}\n")
    
    total_score = 0
    responses = []
    
    for i, q in enumerate(questions, 1):
        print(f"{Fore.CYAN}Question {i}/10: {q['question']}{Style.RESET_ALL}")
        print()
        
        # Display options
        for j, option in enumerate(q['options'], 1):
            print(f"  {j}. {option}")
        print()
        
        # Get user input
        while True:
            try:
                choice = input(f"{Fore.GREEN}Your choice (1-{len(q['options'])}): {Style.RESET_ALL}")
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(q['options']):
                    selected_option = q['options'][choice_num - 1]
                    score = q['scores'][choice_num - 1]
                    total_score += score
                    
                    responses.append({
                        "question": q['question'],
                        "answer": selected_option,
                        "score": score,
                        "category": q['category']
                    })
                    break
                else:
                    print(f"{Fore.RED}Please enter a number between 1 and {len(q['options'])}.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
        
        print(f"{Fore.BLUE}{'─' * 60}{Style.RESET_ALL}\n")
    
    return total_score, responses


def calculate_risk_profile(score: int) -> Dict:
    """Calculate the risk profile based on total score."""
    if score <= 20:
        profile = "Conservative"
        description = """
        You prefer stability and capital preservation over high returns. 
        You're risk-averse and value predictable, steady growth.
        """
        characteristics = [
            "Low risk tolerance",
            "Prefers guaranteed returns",
            "Values capital preservation",
            "Comfortable with modest growth",
            "Prefers liquid investments"
        ]
        investments = [
            "Money Market Funds (MMFs)",
            "High-yield savings accounts", 
            "Treasury bills and bonds",
            "Fixed deposits",
            "Conservative mutual funds"
        ]
        allocation = "Cash/Bonds: 70-80%, Stocks: 20-30%, Alternatives: 0-10%"
        
    elif score <= 35:
        profile = "Balanced"
        description = """
        You seek a balance between growth and security. You're willing to 
        accept moderate risk for potentially higher returns than conservative investments.
        """
        characteristics = [
            "Moderate risk tolerance",
            "Balanced approach to growth and security",
            "Willing to accept some volatility",
            "Long-term investment perspective",
            "Diversification-focused"
        ]
        investments = [
            "Real estate investment trusts (REITs)",
            "Mixed mutual funds",
            "Index funds",
            "Dividend-paying stocks",
            "Balanced portfolios"
        ]
        allocation = "Cash/Bonds: 40-50%, Stocks: 40-50%, Alternatives: 10-20%"
        
    else:  # score > 35
        profile = "Aggressive"
        description = """
        You're willing to take significant risks for potentially high returns. 
        You can handle volatility and have a long-term investment horizon.
        """
        characteristics = [
            "High risk tolerance",
            "Growth-focused mindset",
            "Comfortable with volatility",
            "Long-term investment horizon",
            "Seeks maximum returns"
        ]
        investments = [
            "Cryptocurrency and digital assets",
            "Growth stocks and equity funds",
            "Startup investments and private equity",
            "Commodities and precious metals",
            "International/emerging market funds"
        ]
        allocation = "Cash/Bonds: 10-20%, Stocks: 60-70%, Alternatives: 20-30%"
    
    return {
        "profile": profile,
        "score": score,
        "description": description.strip(),
        "characteristics": characteristics,
        "recommended_investments": investments,
        "suggested_allocation": allocation
    }


def display_results(user_info: Dict, risk_profile: Dict, responses: List[Dict]):
    """Display the assessment results in a formatted manner."""
    print(f"\n{Fore.MAGENTA + Style.BRIGHT}{'=' * 65}")
    print(f"                    ASSESSMENT RESULTS                    ")
    print(f"{'=' * 65}{Style.RESET_ALL}")
    
    # User summary
    print(f"\n{Fore.CYAN}Assessment for: {Style.BRIGHT}{user_info['name']}")
    print(f"{Fore.CYAN}Age: {user_info['age']}")
    print(f"Date: {user_info['date']}{Style.RESET_ALL}")
    
    # Risk profile header
    profile_color = Fore.RED if risk_profile['profile'] == 'Conservative' else \
                   Fore.YELLOW if risk_profile['profile'] == 'Balanced' else Fore.GREEN
    
    print(f"\n{profile_color + Style.BRIGHT}🎯 YOUR RISK PROFILE: {risk_profile['profile'].upper()}")
    print(f"📊 Total Score: {risk_profile['score']}/50{Style.RESET_ALL}")
    
    # Description
    print(f"\n{Fore.BLUE}📋 Profile Description:{Style.RESET_ALL}")
    print(risk_profile['description'])
    
    # Characteristics
    print(f"\n{Fore.BLUE}✨ Key Characteristics:{Style.RESET_ALL}")
    for char in risk_profile['characteristics']:
        print(f"  • {char}")
    
    # Investment recommendations
    print(f"\n{Fore.GREEN}💡 Recommended Investments:{Style.RESET_ALL}")
    for investment in risk_profile['recommended_investments']:
        print(f"  • {investment}")
    
    # Asset allocation
    print(f"\n{Fore.YELLOW}📈 Suggested Asset Allocation:{Style.RESET_ALL}")
    print(f"  {risk_profile['suggested_allocation']}")
    
    # Category breakdown if tabulate is available
    if TABULATE_AVAILABLE:
        print(f"\n{Fore.BLUE}📊 Score Breakdown by Category:{Style.RESET_ALL}")
        
        # Group responses by category
        category_scores = {}
        for response in responses:
            category = response['category'].replace('_', ' ').title()
            if category not in category_scores:
                category_scores[category] = {'total': 0, 'count': 0}
            category_scores[category]['total'] += response['score']
            category_scores[category]['count'] += 1
        
        # Create table data
        table_data = []
        for category, data in category_scores.items():
            avg_score = data['total'] / data['count']
            table_data.append([category, f"{avg_score:.1f}/5.0", f"{data['total']}/{data['count']*5}"])
        
        print(tabulate(table_data, 
                      headers=['Category', 'Avg Score', 'Total Score'],
                      tablefmt='grid'))


def save_results(user_info: Dict, risk_profile: Dict, responses: List[Dict]) -> str:
    """Save the assessment results to a JSON file."""
    # Create results directory if it doesn't exist
    if not os.path.exists('results'):
        os.makedirs('results')
    
    # Prepare data for saving
    save_data = {
        "user_info": user_info,
        "risk_profile": risk_profile,
        "responses": responses,
        "assessment_version": "1.0"
    }
    
    # Generate filename
    safe_name = "".join(c for c in user_info['name'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/finscope_profile_{safe_name}_{date_str}.json"
    
    # Save to file
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        return filename
    except Exception as e:
        print(f"{Fore.RED}Error saving file: {str(e)}{Style.RESET_ALL}")
        return None


def display_tips(profile: str):
    """Display personalized financial tips based on risk profile."""
    tips = {
        "Conservative": [
            "Start with an emergency fund covering 6-12 months of expenses",
            "Consider Treasury bills for guaranteed returns with government backing",
            "Look into Money Market Funds (MMFs) for better rates than savings accounts",
            "Diversify even conservative investments across different banks/institutions",
            "Review and adjust your risk tolerance annually as circumstances change"
        ],
        "Balanced": [
            "Maintain a diversified portfolio across different asset classes",
            "Consider dollar-cost averaging to reduce timing risk",
            "Rebalance your portfolio quarterly to maintain target allocation",
            "Start with index funds for broad market exposure",
            "Keep 3-6 months expenses in liquid emergency funds"
        ],
        "Aggressive": [
            "Never invest more than you can afford to lose in high-risk assets",
            "Research thoroughly before investing in individual stocks or crypto",
            "Consider starting with small amounts in aggressive investments",
            "Maintain some conservative investments for stability",
            "Stay informed about market trends and economic indicators"
        ]
    }
    
    print(f"\n{Fore.BLUE + Style.BRIGHT}💡 PERSONALIZED TIPS FOR {profile.upper()} INVESTORS{Style.RESET_ALL}")
    for tip in tips.get(profile, []):
        print(f"  • {tip}")


def main():
    """Main application function."""
    print_banner()
    
    while True:
        try:
            # Get user information
            user_info = get_user_info()
            
            # Conduct assessment
            questions = get_questions()
            total_score, responses = conduct_assessment(questions)
            
            # Calculate risk profile
            risk_profile = calculate_risk_profile(total_score)
            
            # Display results
            display_results(user_info, risk_profile, responses)
            
            # Display personalized tips
            display_tips(risk_profile['profile'])
            
            # Save results
            print(f"\n{Fore.BLUE}💾 Saving your results...{Style.RESET_ALL}")
            filename = save_results(user_info, risk_profile, responses)
            
            if filename:
                print(f"{Fore.GREEN}✅ Results saved to: {filename}{Style.RESET_ALL}")
            
            # Ask if user wants to retake assessment
            print(f"\n{Fore.MAGENTA}{'─' * 65}{Style.RESET_ALL}")
            retry = input(f"{Fore.CYAN}Would you like to take the assessment again? (y/n): {Style.RESET_ALL}").strip().lower()
            
            if retry not in ['y', 'yes']:
                break
                
            print("\n" + "="*65 + "\n")
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Assessment cancelled by user. Goodbye!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"\n{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please try again.{Style.RESET_ALL}\n")
    
    print(f"\n{Fore.GREEN + Style.BRIGHT}Thank you for using Finscope Profiler!")
    print(f"Remember: This assessment is for educational purposes only.")
    print(f"Always consult with a financial advisor for personalized investment advice.{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}Stay financially literate! 💰📈{Style.RESET_ALL}")


def launch_gui():
    import finscope_profiler_gui

if __name__ == "__main__":
    print("Select mode:")
    print("1. Command Line (CLI)")
    print("2. Graphical (GUI)")
    choice = input("Enter 1 for CLI or 2 for GUI: ").strip()
    if choice == "2":
        launch_gui()
    else:
        main()