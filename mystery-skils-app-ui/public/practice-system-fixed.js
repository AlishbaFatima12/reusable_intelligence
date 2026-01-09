// ═══════════════════════════════════════════════════════════════
// COMPLETE WORKING PRACTICE SYSTEM WITH MCQs
// ═══════════════════════════════════════════════════════════════

// Storage for current practice session
let currentPracticeSession = null;
let assignedTests = []; // Store assigned tests for students

// Show topics list (switch view)
function showTopicsList() {
    document.getElementById('topics-view').classList.remove('hidden');
    document.getElementById('topics-view').style.display = 'flex';
    document.getElementById('practice-view').classList.add('hidden');
    document.getElementById('practice-view').style.display = 'none';
}

// Generate MCQ questions for a topic
function generateMCQs(topicId, topicName) {
    const mcqDatabase = {
        'python-basics': [
            {
                question: "What is Python?",
                options: ["A snake", "A programming language", "A database", "An operating system"],
                correct: 1
            },
            {
                question: "Which symbol is used for comments in Python?",
                options: ["//", "/* */", "#", "<!--"],
                correct: 2
            },
            {
                question: "What is the output of: print(2 + 2)?",
                options: ["22", "4", "Error", "2+2"],
                correct: 1
            }
        ],
        'variables-and-data-types': [
            {
                question: "Which is NOT a valid variable name in Python?",
                options: ["my_var", "2nd_var", "_var", "var2"],
                correct: 1
            },
            {
                question: "What type is the value: 3.14?",
                options: ["int", "float", "string", "boolean"],
                correct: 1
            },
            {
                question: "How do you create a string in Python?",
                options: ["'text'", "[text]", "{text}", "(text)"],
                correct: 0
            }
        ],
        'control-flow': [
            {
                question: "Which keyword starts a conditional statement?",
                options: ["while", "for", "if", "def"],
                correct: 2
            },
            {
                question: "What does 'break' do in a loop?",
                options: ["Pauses the loop", "Exits the loop", "Continues to next iteration", "Crashes the program"],
                correct: 1
            },
            {
                question: "Which loop runs at least once?",
                options: ["for loop", "while loop", "do-while loop (Python doesn't have this)", "if statement"],
                correct: 2
            }
        ],
        'functions': [
            {
                question: "How do you define a function in Python?",
                options: ["function myFunc()", "def myFunc():", "func myFunc()", "define myFunc()"],
                correct: 1
            },
            {
                question: "What does 'return' do in a function?",
                options: ["Prints a value", "Exits and sends back a value", "Deletes a variable", "Creates a loop"],
                correct: 1
            },
            {
                question: "Can a function have multiple return statements?",
                options: ["Yes", "No", "Only in classes", "Only with recursion"],
                correct: 0
            }
        ],
        'data-structures': [
            {
                question: "How do you create an empty list in Python?",
                options: ["{}", "[]", "()", "<>"],
                correct: 1
            },
            {
                question: "What method adds an item to the end of a list?",
                options: ["add()", "append()", "insert()", "push()"],
                correct: 1
            },
            {
                question: "What is a tuple in Python?",
                options: ["Mutable list", "Immutable list", "Dictionary", "Set"],
                correct: 1
            }
        ]
    };

    return mcqDatabase[topicId] || [
        {question: `What is ${topicName}?`, options: ["Option A", "Option B", "Option C", "Option D"], correct: 0},
        {question: `How do you use ${topicName}?`, options: ["Method 1", "Method 2", "Method 3", "Method 4"], correct: 1},
        {question: `Why is ${topicName} important?`, options: ["Reason 1", "Reason 2", "Reason 3", "Reason 4"], correct: 2}
    ];
}

// Student: Start practice for a specific topic
async function startPractice(topicId, topicName) {
    console.log('Starting practice for:', topicId, topicName);

    const userStr = localStorage.getItem('learnflow_user');
    const user = userStr ? JSON.parse(userStr) : { studentId: 'demo-student-001' };

    // Switch to practice view
    document.getElementById('topics-view').classList.add('hidden');
    document.getElementById('topics-view').style.display = 'none';
    document.getElementById('practice-view').classList.remove('hidden');
    document.getElementById('practice-view').style.display = 'flex';

    // Update title
    document.getElementById('practice-topic-title').textContent = `PRACTICE: ${topicName.toUpperCase()}`;

    // Generate MCQs
    const mcqs = generateMCQs(topicId, topicName);

    // Store practice session
    currentPracticeSession = {
        topicId: topicId,
        topicName: topicName,
        questions: mcqs,
        answers: {}
    };

    // Display MCQs
    const questionsContainer = document.getElementById('practice-questions');
    questionsContainer.innerHTML = '';

    mcqs.forEach((mcq, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'mb-4 pb-3 border-b border-gray-800';

        let optionsHTML = '';
        mcq.options.forEach((option, optionIndex) => {
            optionsHTML += `
                <label class="flex items-center gap-2 mb-1 cursor-pointer hover:text-teal-400 transition">
                    <input type="radio" name="question-${index}" value="${optionIndex}" class="text-teal-500">
                    <span class="text-[8px]">${String.fromCharCode(65 + optionIndex)}. ${option}</span>
                </label>
            `;
        });

        questionDiv.innerHTML = `
            <div class="text-green-400 font-bold text-[9px] mb-2">Question ${index + 1}:</div>
            <div class="text-white text-[8px] mb-3">${mcq.question}</div>
            <div class="ml-2">
                ${optionsHTML}
            </div>
        `;

        questionsContainer.appendChild(questionDiv);
    });
}

// Submit student answers and update progress
async function submitAnswers() {
    if (!currentPracticeSession) {
        alert('No active practice session');
        return;
    }

    const userStr = localStorage.getItem('learnflow_user');
    const user = userStr ? JSON.parse(userStr) : { studentId: 'demo-student-001' };

    // Collect and check answers
    let correctCount = 0;
    const totalQuestions = currentPracticeSession.questions.length;

    for (let i = 0; i < totalQuestions; i++) {
        const selected = document.querySelector(`input[name="question-${i}"]:checked`);
        if (selected) {
            const answer = parseInt(selected.value);
            if (answer === currentPracticeSession.questions[i].correct) {
                correctCount++;
            }
        }
    }

    const score = Math.round((correctCount / totalQuestions) * 100);
    const passed = correctCount >= (totalQuestions / 2);

    // Update mastery via Progress Tracker
    try {
        await fetch(`http://localhost:8006/api/v1/mastery/${user.studentId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                student_id: user.studentId,
                topic: currentPracticeSession.topicId,
                interaction_type: 'practice_completed',
                success: passed
            })
        });

        // Show results
        alert(`✅ Practice Complete!\n\nCorrect: ${correctCount}/${totalQuestions}\nScore: ${score}%\n\nYour mastery has been updated!`);

        // Refresh mastery data
        await fetchMasteryData();

        // Go back to topics list
        showTopicsList();

    } catch (error) {
        alert('Failed to update mastery: ' + error.message);
        console.error('Submit error:', error);
    }
}

// ═══════════════════════════════════════════════════════════════
// TEACHER FUNCTIONS
// ═══════════════════════════════════════════════════════════════

let generatedTest = null;

// Teacher: Generate practice test
async function teacherGeneratePractice() {
    console.log('teacherGeneratePractice() called');

    const topic = document.getElementById('practice-topic').value;
    const difficulty = document.getElementById('practice-difficulty').value;
    const count = parseInt(document.getElementById('practice-count').value);

    console.log('Generating test:', {topic, difficulty, count});

    const consoleContent = document.getElementById('console-content');
    if (!consoleContent) {
        alert('Error: Console not found. Make sure you are logged in as teacher.');
        return;
    }

    consoleContent.innerHTML = '<div class="text-yellow-400 text-[9px]">[GENERATING] Creating practice test...</div>';

    // Generate MCQs based on topic
    const mcqs = generateMCQs(topic, topic.replace(/-/g, ' '));

    generatedTest = {
        topic: topic,
        difficulty: difficulty,
        questions: mcqs.slice(0, count)
    };

    // Display generated test
    consoleContent.innerHTML = '';
    const header = document.createElement('div');
    header.className = 'text-cyan-400 font-bold text-[9px] mb-2';
    header.textContent = `✅ GENERATED TEST: ${topic.toUpperCase()}`;
    consoleContent.appendChild(header);

    generatedTest.questions.forEach((q, index) => {
        const qDiv = document.createElement('div');
        qDiv.className = 'mb-2 pb-2 border-b border-gray-800 text-[8px]';
        qDiv.innerHTML = `
            <div class="text-green-400 font-bold">Q${index + 1}: ${q.question}</div>
            ${q.options.map((opt, i) => `<div class="text-gray-400 ml-2">${String.fromCharCode(65 + i)}. ${opt}</div>`).join('')}
            <div class="text-yellow-400 text-[7px] mt-1">Correct: ${String.fromCharCode(65 + q.correct)}</div>
        `;
        consoleContent.appendChild(qDiv);
    });

    // Load students for assignment
    await loadStudentsForAssignment();

    const readyMsg = document.createElement('div');
    readyMsg.className = 'text-green-400 text-[8px] mt-2 font-bold border border-green-900 p-2';
    readyMsg.textContent = '✓ Ready to assign! Select students below.';
    consoleContent.appendChild(readyMsg);
}

// Load students into assignment list
async function loadStudentsForAssignment() {
    try {
        const response = await fetch('/api/auth/students');
        const data = await response.json();

        const assignList = document.getElementById('assign-student-list');
        if (!assignList) return;

        assignList.innerHTML = '';

        if (data.success && data.students && data.students.length > 0) {
            data.students.forEach(student => {
                const checkbox = document.createElement('div');
                checkbox.className = 'mb-1 text-white';
                checkbox.innerHTML = `
                    <label class="flex items-center gap-2 cursor-pointer hover:text-teal-400 transition">
                        <input type="checkbox" class="assign-checkbox" value="${student.studentId}" data-name="${student.name}">
                        <span class="text-[9px]">${student.name}</span>
                    </label>
                `;
                assignList.appendChild(checkbox);
            });
        }
    } catch (error) {
        console.error('Failed to load students:', error);
    }
}

// Assign practice to selected students
function assignPracticeToSelected() {
    if (!generatedTest) {
        alert('Please generate a practice test first');
        return;
    }

    const checkboxes = document.querySelectorAll('.assign-checkbox:checked');
    if (checkboxes.length === 0) {
        alert('Please select at least one student');
        return;
    }

    const assigned = [];
    checkboxes.forEach(cb => {
        assigned.push(cb.dataset.name);

        // Store assignment (in localStorage for now, should be database)
        const assignment = {
            studentId: cb.value,
            test: generatedTest,
            assignedAt: new Date().toISOString(),
            completed: false
        };
        assignedTests.push(assignment);
    });

    // Save to localStorage
    localStorage.setItem('learnflow_assigned_tests', JSON.stringify(assignedTests));

    const consoleContent = document.getElementById('console-content');
    const successMsg = document.createElement('div');
    successMsg.className = 'text-green-400 font-bold text-[9px] mt-3 p-2 border border-green-900';
    successMsg.innerHTML = `
        <div>✅ Test Assigned Successfully!</div>
        <div class="text-white font-normal mt-1">Assigned to: ${assigned.join(', ')}</div>
        <div class="text-[7px] text-gray-400 mt-1">Students will see this when they login</div>
    `;
    consoleContent.appendChild(successMsg);

    alert(`✅ Test assigned to: ${assigned.join(', ')}\n\nStudents will see a notification when they login!`);
}

// Auto-assign practice to struggling students
async function autoAssignPractice() {
    console.log('autoAssignPractice() called');

    // Get struggling students
    const studentsResponse = await fetch('/api/auth/students');
    const studentsData = await studentsResponse.json();

    if (!studentsData.success) return;

    const strugglingStudents = [];

    // Check each student's mastery
    for (const student of studentsData.students) {
        try {
            const masteryResponse = await fetch(`http://localhost:8006/api/v1/mastery/${student.studentId}`);
            const masteryData = await masteryResponse.json();

            if (masteryData.overall_mastery < 0.4) {
                strugglingStudents.push(student);
            }
        } catch (err) {
            console.error('Error checking student:', student.name, err);
        }
    }

    if (strugglingStudents.length === 0) {
        alert('No struggling students found!');
        return;
    }

    // Generate practice for struggling topics
    const topic = 'python-basics'; // Default topic
    const mcqs = generateMCQs(topic, 'Python Basics');

    const test = {
        topic: topic,
        difficulty: 'easy',
        questions: mcqs
    };

    // Assign to all struggling students
    strugglingStudents.forEach(student => {
        const assignment = {
            studentId: student.studentId,
            test: test,
            assignedAt: new Date().toISOString(),
            completed: false,
            autoAssigned: true
        };
        assignedTests.push(assignment);
    });

    localStorage.setItem('learnflow_assigned_tests', JSON.stringify(assignedTests));

    const names = strugglingStudents.map(s => s.name).join(', ');
    alert(`✅ Auto-assigned practice to: ${names}\n\nStudents will see notification!`);

    const consoleContent = document.getElementById('console-content');
    consoleContent.innerHTML = `
        <div class="text-green-400 font-bold text-[9px] p-2 border border-green-900">
            ✅ Auto-Assigned Practice
            <div class="text-white font-normal mt-2">Assigned to: ${names}</div>
            <div class="text-[7px] text-gray-400 mt-1">Topic: Python Basics (Easy)</div>
        </div>
    `;
}

// Check for assigned tests (student login)
function checkAssignedTests() {
    const userStr = localStorage.getItem('learnflow_user');
    if (!userStr) return;

    const user = JSON.parse(userStr);
    if (user.role !== 'student') return;

    const assignedTestsStr = localStorage.getItem('learnflow_assigned_tests');
    if (!assignedTestsStr) return;

    const tests = JSON.parse(assignedTestsStr);
    const myTests = tests.filter(t => t.studentId === user.studentId && !t.completed);

    if (myTests.length > 0) {
        // Show notification
        setTimeout(() => {
            const count = myTests.length;
            alert(`📚 You have ${count} new assignment${count > 1 ? 's' : ''}!\n\nCheck your practice panel to start.`);
        }, 2000);
    }
}
