"""
EduGenie Deterministic Offline Generators
Provides robust, high-quality, reproducible responses for Demo Mode and Live API Fallback.
Ensures the entire application runs seamlessly offline and during automated testing/demos.
"""

from typing import List, Dict, Any
import re

def generate_demo_qa(question: str) -> str:
    """Provides factual, concise answers for educational queries."""
    q_lower = question.strip().lower()
    
    if "largest ocean" in q_lower or "biggest ocean" in q_lower:
        return (
            "The Pacific Ocean is the largest and deepest ocean on Earth. "
            "It spans over 63 million square miles (165 million square kilometers), "
            "covering more than 30% of the Earth's total surface area and holding over half of the world's open water."
        )
    elif "photosynthesis" in q_lower:
        return (
            "Photosynthesis is the biological process by which green plants, algae, and some bacteria "
            "convert sunlight, carbon dioxide (CO₂), and water (H₂O) into chemical energy in the form of glucose (sugar) "
            "and release oxygen (O₂) as a byproduct."
        )
    elif "gravity" in q_lower:
        return (
            "Gravity is a fundamental natural force of attraction between all objects with mass. "
            "It was famously formulated by Sir Isaac Newton in 1687 with the Universal Law of Gravitation, "
            "and later re-described by Albert Einstein in 1915 as the curvature of spacetime."
        )
    elif "pythagoras" in q_lower:
        return (
            "The Pythagoras theorem states that in any right-angled triangle, the square of the hypotenuse (c) "
            "equals the sum of the squares of the other two sides (a and b): a² + b² = c²."
        )
    elif "speed of light" in q_lower:
        return (
            "The speed of light in a vacuum is exactly 299,792,458 meters per second (approximately 300,000 km/s or 186,282 miles per second)."
        )
    else:
        # High quality generic answer
        return (
            f"Regarding '{question.strip()}': In educational science and research, this topic centers on fundamental principles "
            f"governing core domain concepts, logical structures, and practical applications. "
            f"Key principles include foundational definitions, analytical methods, and evidence-based problem solving."
        )

def generate_demo_explanation(topic: str, backend: str = "gemini") -> str:
    """Generates simple, student-friendly concept explanations with analogies."""
    t_lower = topic.strip().lower()
    
    if "quantum computing" in t_lower:
        return (
            "### 🔬 Quantum Computing Explained Simply\n\n"
            "**What is it?**\n"
            "Imagine your regular computer is like a light switch that can only be either **OFF (0)** or **ON (1)**. "
            "A quantum computer uses special particles called **Qubits** (quantum bits) that can be **both 0 and 1 at the same time**!\n\n"
            "**Key Concepts Made Easy:**\n"
            "1. **Superposition:** Like a spinning coin in mid-air—it is neither heads nor tails until it lands. This lets the computer explore millions of possibilities simultaneously.\n"
            "2. **Entanglement:** Two qubits can be magically linked so that changing one instantly changes the other, no matter the distance.\n\n"
            "**Real-World Analogy:**\n"
            "If a standard computer tries to escape a maze, it tests one path at a time. A quantum computer enters **every path at the exact same moment** and finds the exit in seconds!\n\n"
            "**Why it Matters:**\n"
            "Quantum computers will revolutionize medicine discovery, ultra-secure encryption, weather forecasting, and artificial intelligence."
        )
    elif "binary search" in t_lower:
        return (
            "### 🔍 Binary Search Algorithm Explained Simply\n\n"
            "**What is it?**\n"
            "Binary search is an ultra-fast algorithm used to find a specific item in a **sorted list** by repeatedly cutting the search area in half.\n\n"
            "**The Phonebook Analogy:**\n"
            "Imagine searching for the name *'Smith'* in a 1,000-page phonebook:\n"
            "- **Slow Way (Linear Search):** Turn page 1, then page 2, then page 3... you might have to flip 800 pages.\n"
            "- **Smart Way (Binary Search):** Open the book right in the middle (page 500, letter *'M'*). Since *'S'* comes after *'M'*, throw away the first 500 pages! Repeat with the remaining half.\n\n"
            "**Step-by-Step Logic:**\n"
            "1. Look at the middle element of the sorted list.\n"
            "2. If the middle is your target, you're done!\n"
            "3. If your target is smaller, search only the left half.\n"
            "4. If your target is larger, search only the right half.\n\n"
            "**Time Complexity:**\n"
            "It runs in **O(log n)** time. In a list of 1,000,000 numbers, binary search finds the answer in at most **20 comparisons**!"
        )
    elif "photosynthesis" in t_lower:
        return (
            "### 🌿 Photosynthesis Explained Simply\n\n"
            "**What is it?**\n"
            "Photosynthesis is how plants act as nature's solar-powered food factories!\n\n"
            "**The Recipe for Plant Food:**\n"
            "- **Ingredients:** Sunlight ☀️ + Water (H₂O) 💧 from roots + Carbon Dioxide (CO₂) 💨 from air.\n"
            "- **Cooking Location:** Inside green leaf cells called **Chloroplasts**, which contain **Chlorophyll**.\n"
            "- **Final Dish:** Glucose (energy food for the plant) + Oxygen (O₂) released into the atmosphere for humans and animals to breathe!\n\n"
            "**Chemical Formula:**\n"
            "`6CO₂ + 6H₂O + Sunlight ➔ C₆H₁₂O₆ + 6O₂`"
        )
    else:
        return (
            f"### 💡 Understanding {topic.title()} Simply\n\n"
            f"**Core Concept:**\n"
            f"**{topic.title()}** is an essential subject in modern learning. It focuses on how fundamental components interact "
            f"systematically to produce consistent and predictable outcomes.\n\n"
            f"**How to Think About It:**\n"
            f"- **Foundations:** Start with basic rules and primary building blocks.\n"
            f"- **Mechanics:** Observe cause-and-effect relationships within the system.\n"
            f"- **Practical Application:** Apply the concepts to solve real-world problems step by step.\n\n"
            f"**Key Takeaway:**\n"
            f"Mastering {topic.title()} begins with breaking down complex ideas into simple, manageable building blocks."
        )

def generate_demo_summary(text: str) -> str:
    """Generates concise educational summaries with core takeaways."""
    t_lower = text.strip().lower()
    
    if "industrial revolution" in t_lower:
        return (
            "### 🏭 Summary: The Industrial Revolution\n\n"
            "**Key Takeaways:**\n"
            "• **Era of Transformation:** Began in Great Britain during the late 18th century (c. 1760–1840) and marked the transition from handcraft agrarian economies to machine-driven industrial production.\n"
            "• **Key Inventions:** Technological breakthroughs included James Watt's improved steam engine, James Hargreaves' Spinning Jenny, and mechanized textile mills.\n"
            "• **Socioeconomic Impact:** Led to rapid urbanization as rural populations migrated to factory cities, creating new social classes, modern transportation networks (railways and steamships), and mass consumer markets.\n"
            "• **Global Legacy:** Laid the structural foundation for modern capitalism, international trade, and technological innovation, while also introducing modern labor and environmental challenges."
        )
    elif len(text.strip()) > 50:
        # Extract sentences and make clean summary
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 10]
        summary_points = sentences[:3] if len(sentences) >= 3 else sentences
        bullets = "\n".join([f"• {pt}." for pt in summary_points])
        return (
            f"### 📋 Key Summary Points\n\n"
            f"{bullets}\n\n"
            f"**Core Conclusion:** The passage outlines fundamental concepts, highlighting the relationship between core drivers and overall practical outcomes."
        )
    else:
        return (
            f"### 📋 Summary\n\n"
            f"• Key Point: {text.strip()}\n"
            f"• The passage provides a concise overview of the core subject matter."
        )

def generate_demo_quiz(text_or_topic: str) -> List[Dict[str, Any]]:
    """Generates exactly 3 MCQs with 4 options each, where answer matches an option string."""
    q_lower = text_or_topic.strip().lower()
    
    if "pythagor" in q_lower or "triangle" in q_lower:
        return [
            {
                "question": "What is the standard algebraic formula for the Pythagoras theorem?",
                "options": [
                    "a² + b² = c²",
                    "a² - b² = c²",
                    "a + b = c",
                    "2a + 2b = c²"
                ],
                "answer": "a² + b² = c²"
            },
            {
                "question": "The Pythagoras theorem applies specifically to which type of triangle?",
                "options": [
                    "Equilateral triangle",
                    "Right-angled triangle",
                    "Isosceles triangle",
                    "Obtuse-angled triangle"
                ],
                "answer": "Right-angled triangle"
            },
            {
                "question": "If the two legs of a right triangle measure 3 cm and 4 cm, what is the length of the hypotenuse?",
                "options": [
                    "5 cm",
                    "6 cm",
                    "7 cm",
                    "8 cm"
                ],
                "answer": "5 cm"
            }
        ]
    elif "ocean" in q_lower or "water" in q_lower:
        return [
            {
                "question": "Which of the following is the largest and deepest ocean on Earth?",
                "options": [
                    "Atlantic Ocean",
                    "Indian Ocean",
                    "Pacific Ocean",
                    "Arctic Ocean"
                ],
                "answer": "Pacific Ocean"
            },
            {
                "question": "What is the deepest known location in Earth's oceans?",
                "options": [
                    "Mariana Trench (Challenger Deep)",
                    "Puerto Rico Trench",
                    "Java Trench",
                    "Tonga Trench"
                ],
                "answer": "Mariana Trench (Challenger Deep)"
            },
            {
                "question": "Approximately what percentage of the Earth's surface is covered by oceans?",
                "options": [
                    "50%",
                    "71%",
                    "85%",
                    "92%"
                ],
                "answer": "71%"
            }
        ]
    elif "photosynthesis" in q_lower or "plant" in q_lower:
        return [
            {
                "question": "Which pigment in plant leaves absorbs sunlight for photosynthesis?",
                "options": [
                    "Chlorophyll",
                    "Carotenoid",
                    "Anthocyanin",
                    "Hemoglobin"
                ],
                "answer": "Chlorophyll"
            },
            {
                "question": "What gas is released into the atmosphere as a byproduct of photosynthesis?",
                "options": [
                    "Carbon Dioxide",
                    "Nitrogen",
                    "Oxygen",
                    "Methane"
                ],
                "answer": "Oxygen"
            },
            {
                "question": "In which plant cell organelle does photosynthesis primarily occur?",
                "options": [
                    "Mitochondria",
                    "Chloroplast",
                    "Ribosome",
                    "Nucleus"
                ],
                "answer": "Chloroplast"
            }
        ]
    else:
        topic_name = text_or_topic.strip()[:30].title() or "Computer Science"
        return [
            {
                "question": f"What is a primary principle associated with {topic_name}?",
                "options": [
                    "Systematic decomposition into modular elements",
                    "Random execution without structured logic",
                    "Ignoring input data validation",
                    "Complete reliance on manual calculation"
                ],
                "answer": "Systematic decomposition into modular elements"
            },
            {
                "question": f"Which approach yields optimal results when studying {topic_name}?",
                "options": [
                    "Active recall and hands-on practice",
                    "Passive skimming without exercises",
                    "Skipping prerequisite fundamentals",
                    "Memorizing answers without understanding"
                ],
                "answer": "Active recall and hands-on practice"
            },
            {
                "question": f"How is performance typically evaluated in {topic_name}?",
                "options": [
                    "Efficiency, accuracy, and scalability",
                    "Only by code file size",
                    "Strictly by execution timestamp",
                    "Alphabetical order of functions"
                ],
                "answer": "Efficiency, accuracy, and scalability"
            }
        ]

def generate_demo_learning_path(topic: str) -> str:
    """Generates structured beginner-to-advanced learning roadmaps."""
    t_lower = topic.strip().lower()
    
    if "sql" in t_lower or "database" in t_lower:
        return (
            "### 🗺️ Structured Learning Roadmap: SQL & Relational Databases\n\n"
            "#### 🟢 Stage 1: Beginner Fundamentals (Weeks 1–2)\n"
            "- **Core Concepts:** Relational Database concepts, Tables, Rows, Columns, Primary & Foreign Keys.\n"
            "- **SQL Commands:** `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `INSERT`, `UPDATE`, `DELETE`.\n"
            "- **Estimated Time:** 10–12 Hours\n"
            "- **Recommended Resources:**\n"
            "  - *Interactive:* W3Schools SQL Tutorial & Mode Analytics SQL Guide\n"
            "  - *Practice:* SQLBolt Interactive Exercises (free interactive sandbox)\n\n"
            "#### 🟡 Stage 2: Intermediate Data Manipulation (Weeks 3–4)\n"
            "- **Core Concepts:** Table Joins (`INNER`, `LEFT`, `RIGHT`, `FULL OUTER`), Aggregations (`GROUP BY`, `HAVING`), Set Operations (`UNION`, `INTERSECT`).\n"
            "- **Advanced Filters:** Subqueries, `CASE WHEN` conditional statements, Date/String functions.\n"
            "- **Estimated Time:** 15–18 Hours\n"
            "- **Recommended Resources:**\n"
            "  - *Platform:* LeetCode Database (Easy/Medium) & HackerRank SQL Track\n"
            "  - *Video:* freeCodeCamp 4-Hour SQL Database Course\n\n"
            "#### 🔴 Stage 3: Advanced Optimization & Analytics (Weeks 5–6)\n"
            "- **Core Concepts:** Window Functions (`ROW_NUMBER`, `RANK`, `LEAD`, `LAG`), Common Table Expressions (CTEs), Indexing, Query Execution Plans (`EXPLAIN ANALYZE`), Stored Procedures & Triggers.\n"
            "- **Estimated Time:** 20–25 Hours\n"
            "- **Recommended Resources:**\n"
            "  - *Book:* 'Learning SQL' by Alan Beaulieu (O'Reilly)\n"
            "  - *Hands-on Project:* Build an E-Commerce Analytics Schema in PostgreSQL/MySQL\n\n"
            "#### 🎯 Milestone Project\n"
            "Design and build a multi-table database schema with normalized tables, complex analytical queries with window functions, and indexing strategies for sub-second performance."
        )
    elif "python" in t_lower:
        return (
            "### 🗺️ Structured Learning Roadmap: Python Programming\n\n"
            "#### 🟢 Stage 1: Python Basics (Weeks 1–2)\n"
            "- **Core Concepts:** Variables, Data Types, Conditionals (`if-else`), Loops (`for`, `while`), Functions.\n"
            "- **Estimated Time:** 12 Hours\n"
            "- **Resources:** Official Python Docs, Automate the Boring Stuff with Python.\n\n"
            "#### 🟡 Stage 2: Data Structures & OOP (Weeks 3–4)\n"
            "- **Core Concepts:** Lists, Dictionaries, Sets, Tuples, Object-Oriented Programming (Classes, Inheritance), Error Handling (`try-except`).\n"
            "- **Estimated Time:** 18 Hours\n"
            "- **Resources:** Python Crash Course, LeetCode Easy problems.\n\n"
            "#### 🔴 Stage 3: Frameworks & Real Projects (Weeks 5–6)\n"
            "- **Core Concepts:** FastAPI / Flask web backends, Database connectivity (SQLAlchemy), Unit testing (pytest), API integration.\n"
            "- **Estimated Time:** 25 Hours\n"
            "- **Resources:** FastAPI Official Tutorial, RealPython.com projects."
        )
    else:
        return (
            f"### 🗺️ Structured Learning Roadmap: {topic.title()}\n\n"
            f"#### 🟢 Stage 1: Foundations & Core Concepts (Weeks 1–2)\n"
            f"- **Focus:** Master basic definitions, syntax, and foundational theories.\n"
            f"- **Estimated Time:** 10–12 Hours\n"
            f"- **Recommended Resources:** Introductory documentation, video crash courses, hands-on beginner tutorials.\n\n"
            f"#### 🟡 Stage 2: Practical Application & Intermediate Skills (Weeks 3–4)\n"
            f"- **Focus:** Build mini-projects, solve algorithmic challenges, and understand standard patterns.\n"
            f"- **Estimated Time:** 15–20 Hours\n"
            f"- **Recommended Resources:** Interactive problem-solving platforms, guided code-alongs.\n\n"
            f"#### 🔴 Stage 3: Advanced Mastery & System Architecture (Weeks 5–6)\n"
            f"- **Focus:** Performance tuning, edge-case optimization, production-grade deployment.\n"
            f"- **Estimated Time:** 20–25 Hours\n"
            f"- **Recommended Resources:** Technical reference manuals, open-source repositories, capstone projects."
        )
