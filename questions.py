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
        mid_coeff = '- '+ str(abs(a+b)) + 'x '
    elif a + b == 0:
        mid_coeff = ''
    elif a + b == 1:
        mid_coeff = '- x '
    elif a+b == -1:
        mid_coeff = '+ x '
    else:
        mid_coeff = '+ ' + str(abs(a+b)) + 'x '
    if a*b > 0:
        end_coeff = '+ ' + str(abs(a*b))
    elif a*b == 0:
        end_coeff = ''
    else:
        end_coeff ='- ' + str(abs(a*b))
     
    question = "What are the roots of " + '\\(x^2 ' + mid_coeff + end_coeff + '\\)' + '?'

    real_answer = str(a) + ',' + str(b)
    options = [real_answer, str((a+b)) + ',' + str(a*b), str(c) + ',' + str(d), str(e) + ',' + str(f)]
    rand.shuffle(options)
    return {'question': question, 'options': options, 'answer': real_answer}

def gradefunction(success):
    if success >= 133*100/160:
        return str(9)
    if success >= 122*100/160:
        return str(8)
    if success >= 111*100/160:
        return str(7)
    if success >= 99*100/160:
        return str(6)
    if success >= 87*100/160:
        return str(5)
    if success >= 75*100/160:
        return str(4)
    if success >= 54*100/160:
        return str(3)
    if success >= 33*100/160:
        return str(2)
    if success >= 12*100/160:
        return str(1)
    else:
        return 'U'