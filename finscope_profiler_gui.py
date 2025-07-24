import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

# --- Logic from finscope_profiler.py (adapted) ---

def get_questions():
    return [
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

def calculate_risk_profile(score):
    if score <= 20:
        profile = "Conservative"
        description = (
            "You prefer stability and capital preservation over high returns. "
            "You're risk-averse and value predictable, steady growth."
        )
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
        description = (
            "You seek a balance between growth and security. You're willing to "
            "accept moderate risk for potentially higher returns than conservative investments."
        )
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
    else:
        profile = "Aggressive"
        description = (
            "You're willing to take significant risks for potentially high returns. "
            "You can handle volatility and have a long-term investment horizon."
        )
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
        "description": description,
        "characteristics": characteristics,
        "recommended_investments": investments,
        "suggested_allocation": allocation
    }

def get_tips(profile):
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
    return tips.get(profile, [])

def save_results(user_info, risk_profile, responses):
    if not os.path.exists('results'):
        os.makedirs('results')
    save_data = {
        "user_info": user_info,
        "risk_profile": risk_profile,
        "responses": responses,
        "assessment_version": "1.0"
    }
    safe_name = "".join(c for c in user_info['name'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/finscope_profile_{safe_name}_{date_str}.json"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        return filename
    except Exception as e:
        return None

# --- Tkinter GUI ---

class FinscopeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Finscope Profiler")
        self.geometry("700x600")
        self.resizable(False, False)
        self.user_info = {}
        self.questions = get_questions()
        self.responses = []
        self.current_question = 0
        self.frames = {}
        self._build_frames()
        self.show_frame("WelcomeFrame")

    def _build_frames(self):
        for F in (WelcomeFrame, UserInfoFrame, QuestionFrame, ResultsFrame):
            frame = F(self)
            self.frames[F.__name__] = frame
            frame.place(relwidth=1, relheight=1)

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()

    def reset(self):
        self.user_info = {}
        self.responses = []
        self.current_question = 0
        self.show_frame("WelcomeFrame")

class WelcomeFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        banner = tk.Label(self, text="FINSCOPE\nPROFILER", font=("Arial Black", 32, "bold"), fg="#00b7c6")
        banner.pack(pady=30)
        tagline = tk.Label(self, text="Know Your Investment Personality", font=("Arial", 16, "italic"), fg="#333")
        tagline.pack(pady=10)
        desc = tk.Label(self, text="This assessment will help you understand your investment risk tolerance and\nsuggest appropriate investment strategies based on your financial behavior, goals, and preferences.", font=("Arial", 12), justify="center")
        desc.pack(pady=10)
        start_btn = ttk.Button(self, text="Start Assessment", command=lambda: master.show_frame("UserInfoFrame"))
        start_btn.pack(pady=30)

class UserInfoFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="User Information", font=("Arial", 20, "bold"), fg="#a020f0").pack(pady=20)
        form = tk.Frame(self)
        form.pack(pady=20)
        tk.Label(form, text="Name:", font=("Arial", 14)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.name_var = tk.StringVar()
        tk.Entry(form, textvariable=self.name_var, font=("Arial", 14)).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(form, text="Age:", font=("Arial", 14)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.age_var = tk.StringVar()
        tk.Entry(form, textvariable=self.age_var, font=("Arial", 14)).grid(row=1, column=1, padx=5, pady=5)
        self.error_lbl = tk.Label(self, text="", fg="red", font=("Arial", 12))
        self.error_lbl.pack()
        next_btn = ttk.Button(self, text="Next", command=self.validate)
        next_btn.pack(pady=20)

    def validate(self):
        name = self.name_var.get().strip()
        age = self.age_var.get().strip()
        if not name:
            self.error_lbl.config(text="Please enter your name.")
            return
        if not age.isdigit() or not (10 <= int(age) <= 100):
            self.error_lbl.config(text="Please enter a valid age (10-100).")
            return
        self.master.user_info = {
            "name": name,
            "age": age,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.error_lbl.config(text="")
        self.master.show_frame("QuestionFrame")

class QuestionFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.q_label = tk.Label(self, text="", font=("Arial", 16, "bold"), wraplength=600, justify="center")
        self.q_label.pack(pady=30)
        self.var = tk.IntVar()
        self.options = []
        for i in range(5):
            rb = tk.Radiobutton(self, text="", variable=self.var, value=i+1, font=("Arial", 14), anchor="w", justify="left")
            rb.pack(fill="x", padx=100, pady=2)
            self.options.append(rb)
        self.error_lbl = tk.Label(self, text="", fg="red", font=("Arial", 12))
        self.error_lbl.pack()
        nav = tk.Frame(self)
        nav.pack(pady=20)
        self.back_btn = ttk.Button(nav, text="Back", command=self.go_back)
        self.back_btn.grid(row=0, column=0, padx=10)
        self.next_btn = ttk.Button(nav, text="Next", command=self.go_next)
        self.next_btn.grid(row=0, column=1, padx=10)

    def on_show(self):
        qn = self.master.current_question
        q = self.master.questions[qn]
        self.q_label.config(text=f"Q{qn+1}/10: {q['question']}")
        self.var.set(0)
        for i, opt in enumerate(q['options']):
            self.options[i].config(text=opt, state="normal")
        for i in range(len(q['options']), 5):
            self.options[i].config(text="", state="disabled")
        if qn == 0:
            self.back_btn.config(state="disabled")
        else:
            self.back_btn.config(state="normal")
        if qn == len(self.master.questions) - 1:
            self.next_btn.config(text="Submit")
        else:
            self.next_btn.config(text="Next")
        self.error_lbl.config(text="")
        # Restore previous answer if available
        if len(self.master.responses) > qn:
            self.var.set(self.master.responses[qn]["choice"])
        else:
            self.var.set(0)

    def go_next(self):
        choice = self.var.get()
        if not (1 <= choice <= 5):
            self.error_lbl.config(text="Please select an option.")
            return
        qn = self.master.current_question
        q = self.master.questions[qn]
        # Save or update response
        if len(self.master.responses) > qn:
            self.master.responses[qn] = {
                "question": q["question"],
                "answer": q["options"][choice-1],
                "score": q["scores"][choice-1],
                "category": q["category"],
                "choice": choice
            }
        else:
            self.master.responses.append({
                "question": q["question"],
                "answer": q["options"][choice-1],
                "score": q["scores"][choice-1],
                "category": q["category"],
                "choice": choice
            })
        if qn == len(self.master.questions) - 1:
            self.master.show_frame("ResultsFrame")
        else:
            self.master.current_question += 1
            self.master.show_frame("QuestionFrame")

    def go_back(self):
        if self.master.current_question > 0:
            self.master.current_question -= 1
            self.master.show_frame("QuestionFrame")

class ResultsFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.title_lbl = tk.Label(self, text="Assessment Results", font=("Arial", 20, "bold"), fg="#a020f0")
        self.title_lbl.pack(pady=20)
        self.summary = tk.Label(self, text="", font=("Arial", 14), justify="left")
        self.summary.pack(pady=10)
        self.profile_lbl = tk.Label(self, text="", font=("Arial", 16, "bold"))
        self.profile_lbl.pack(pady=10)
        self.desc_lbl = tk.Label(self, text="", font=("Arial", 12), wraplength=600, justify="left")
        self.desc_lbl.pack(pady=10)
        self.char_lbl = tk.Label(self, text="", font=("Arial", 12), justify="left")
        self.char_lbl.pack(pady=5)
        self.inv_lbl = tk.Label(self, text="", font=("Arial", 12), justify="left")
        self.inv_lbl.pack(pady=5)
        self.alloc_lbl = tk.Label(self, text="", font=("Arial", 12), justify="left")
        self.alloc_lbl.pack(pady=5)
        self.tips_lbl = tk.Label(self, text="", font=("Arial", 12), fg="#0077b6", justify="left")
        self.tips_lbl.pack(pady=10)
        nav = tk.Frame(self)
        nav.pack(pady=20)
        ttk.Button(nav, text="Save Results", command=self.save_results).grid(row=0, column=0, padx=10)
        ttk.Button(nav, text="Retake Assessment", command=self.retake).grid(row=0, column=1, padx=10)
        ttk.Button(nav, text="Exit", command=self.quit_app).grid(row=0, column=2, padx=10)

    def on_show(self):
        user = self.master.user_info
        responses = self.master.responses
        total_score = sum(r["score"] for r in responses)
        risk_profile = calculate_risk_profile(total_score)
        self.risk_profile = risk_profile
        self.summary.config(text=f"Assessment for: {user['name']}\nAge: {user['age']}\nDate: {user['date']}\nTotal Score: {risk_profile['score']}/50")
        self.profile_lbl.config(text=f"🎯 Your Risk Profile: {risk_profile['profile']}")
        self.desc_lbl.config(text=f"{risk_profile['description']}")
        self.char_lbl.config(text="Key Characteristics:\n  • " + "\n  • ".join(risk_profile['characteristics']))
        self.inv_lbl.config(text="Recommended Investments:\n  • " + "\n  • ".join(risk_profile['recommended_investments']))
        self.alloc_lbl.config(text=f"Suggested Asset Allocation:\n  {risk_profile['suggested_allocation']}")
        tips = get_tips(risk_profile['profile'])
        self.tips_lbl.config(text="Personalized Tips:\n  • " + "\n  • ".join(tips))

    def save_results(self):
        user = self.master.user_info
        responses = self.master.responses
        total_score = sum(r["score"] for r in responses)
        risk_profile = calculate_risk_profile(total_score)
        filename = save_results(user, risk_profile, responses)
        if filename:
            messagebox.showinfo("Saved", f"Results saved to: {filename}")
        else:
            messagebox.showerror("Error", "Failed to save results.")

    def retake(self):
        self.master.reset()

    def quit_app(self):
        self.master.destroy()

if __name__ == "__main__":
    app = FinscopeApp()
    app.mainloop() 