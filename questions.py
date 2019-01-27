import random as rand
import math
def questiontype1(level = 2):
    elements = []
    for i in range(4):
        elements.append(int(10*level*rand.random()) + 1)
    question = "What is " + str(elements[0]) + "/" + str(elements[1]) + " + " + str(elements[2]) + "/" + str(elements[3]) + " in its simplest form?"
    answers = []
    top = elements[0]*elements[3] + elements[1]*elements[2]
    bottom = elements[1]*elements[3]
    gcd = math.gcd(top, bottom)
    top = top/gcd
    bottom = bottom/gcd
    answers.append(str(int(top)) + "/" + str(int(bottom)))
    real_answer = str(int(top)) + "/" + str(int(bottom))
    top = elements[0]*elements[2]
    bottom = elements[1]*elements[3]
    gcd = math.gcd(top, bottom)
    top = top/gcd
    bottom = bottom/gcd
    answers.append(str(int(top)) + "/" + str(int(bottom)))
    final2 = []
    for i in range(4):
        final2.append(int(10*level*rand.random()) + 1)
    answers.append(str(final2[0]) + "/" + str(final2[1]))
    answers.append(str(final2[2]) + "/" + str(final2[3]))
    rand.shuffle(answers)
    options = answers
    return {'question': question, 'options': options, 'answer': real_answer}

def questiontype2(level = 1):
    a = int(10 * level * rand.random() + 1) - 5*level
    b = int(10 * level * rand.random() + 1) - 5*level
    c = int(10 * level * rand.random() + 1) - 5*level
    d = int(10 * level * rand.random() + 1) - 5*level
    e = int(10 * level * rand.random() + 1) - 5*level
    f = int(10 * level * rand.random() + 1) - 5*level
    if a + b > 0:
        question = "What are the roots of " + '\\(x^2 ' + '- ' + str((a+b)) + 'x ' +'+ ' + str(a*b) + '\\)'
    else:
        question = "What are the roots of " + '\\(x^2 ' + '+ ' + str(-(a + b)) + 'x ' + '+ ' + str(a * b) + '\\)'
    real_answer = str(a) + ',' + str(b)
    options = [real_answer, str((a+b)) + ',' + str(a*b), str(c) + ',' + str(d), str(e) + ',' + str(f)]
    rand.shuffle(options)
    return {'question': question, 'options': options, 'answer': real_answer}