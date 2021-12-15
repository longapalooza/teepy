=====
TEEPy
=====

TEEPy stands for Tech Engineering Exam in Python. TEEPy's aim is to make an
easy-to-use framework to create clean and professional-looking exams or
assessments with a focus on STEM (Science, Technology, Engineering, and Math)
related topics. There are two intended end-users of TEEPy, question creators
(QCs) and assessment creators (ACs). QCs create individual questions or problems
that will be used in a particular assessment that an AC will use to create the
overall assessment. TEEPy accomplishes these goals by generating all question
and assessment content as HTML and then rendering the HTML to create PDFs.
TEEPy supports the use of LaTex_ (via MathJax_) as well as the use of units
(using the package pint_). TEEPy is capable of randomizing question placement
and answer choices to questions.

Installation
============

Installation is a simple matter of

.. code-block:: bash

    $ pip install teepy

and then enjoy!

Roles
=====

There are two roles that an end-user of TEEPy can assume, question creator (QC)
or assessment creator (AC). QCs deal solely with individual questions or problem
creation. ACs deal with the assessment as a whole. ACs take one or more
questions created by QCs and make an assessment out of the selected questions.

Question Creator (QC)
---------------------

The goal of a QC is to create individual questions that are self-contained. The
content and calculations in the individual question file will not interact with
content and calculations performed in another question file. Each question file
must contain two function definitions, a :code:`PROBLEM()` function and a
:code:`CHOICES()` function. Each of these functions takes one argument, an index
value variable. The index value is used to create different versions of a
particular question. The :code:`PROBLEM()` function uses the function's
docstring to define the problem statement and should return a dictionary
containing at least a  key of :code:`answer`. If the question has no answer
(e.g., in the case of an open-ended question), a :code:`None` may be returned
from the :code:`PROBLEM()` function. An example of an open-ended question is
shown below.

.. code-block:: python

    # An open-ended question
    def PROBLEM(ind):
        '''What is the meaning of life?'''
        
        return None

Even if there are no different versions of the question, the :code:`PROBLEM()`
should be a function of the index variable :code:`ind`. 

In the event a question does have a correct answer (or answers), the value of
the key :code:`answer` should be a single value or a list of values (in the case
of a multiple answer problem). An example of a single answer question is shown
below.

.. code-block:: python

    # A single answer question
    def PROBLEM(ind):
        '''What color is the sky?'''
        
        answer = 'Blue'
        
        return {'answer': answer}

An example of a multiple-answer question is shown below.

.. code-block:: python

    # A multiple-answer question
    def PROBLEM(ind):
        '''How many licks does it take to get to the center of a Tootsie Pop?'''
        
        answer = ['3', 'The world may never know.']
        
        return {'answer': answer}

The return value of :code:`PROBLEM()` may also contain a key of :code:`given`.
The value of the key :code:`given` should be a dictionary that includes any
variables used in the question statement. An example of using a given variable
is shown below.

.. code-block:: python

    # A question is a given variable
    def PROBLEM(find):
        '''A {object} is an example of what?'''
        
        obj = ['dog', 'carrot', 'diamond'] 
        
        answers = ['Animal', 'Vegatable', 'Mineral']
        
        given = {'object': obj[ind]}
        
        return {'answer': answers[ind], 'given': given}

It should be noted in the example above that three different versions of the
questions may be created by simply changing the :code:`ind` variable to a value
of zero, one, or two. Units may also be used in the :code:`PROBLEM()` function.
An example of utilizing units is shown below.

.. code-block:: python

    import teepy
    
    def PROBLEM(find):
        '''If points A, B, and C lie along a straight line in that order,
    and the distance between point A and B is $ {L1} $, and the distance
    between point B and C is $ {L2} $, what is the distance between point
    A and C?'''
        
        L1s = [1, 2, 3, 4]
        L2s = [5, 6, 7, 8]
        
        L1 = teepy.define_unit(L1s[ind], 'ft')
        L2 = teepy.define_unit(L2s[ind], 'cm')
        
        L = L1 + L2
        
        answer = L.to('m')
        given = {'L1': L1,
                 'L2': L2}
        
        return {'answer': answer, 'given': given}

There are a few things to note about the example above. If a given variable has
units, the rendered version of the variable (i.e., what is in the problem
statement) needs to be enclosed in dollar signs. The units of a given variable
get converted into LaTeX. LaTeX code that is not enclosed in dollar signs will
not be rendered as LaTeX. The TEEPy function :code:`define_unit` may be used to
assign units to a variable. This function is :code:`pint`'s :code:`Q_` function
(please refer to :code:`pint`'s documentation on how to use it). Once units have
been assigned to a variable, calculations performed with those variables will
automatically perform the necessary conversions when dealing with different
types of units.

The :code:`CHOICES()` function must return a :code:`None` value, or a dictionary
containing the key :code:`choices`. No multiple-choice choices will be displayed
if :code:`CHOICES()` returns a :code:`None` value. An open-ended question is
typically when this is needed. Below is an example of a :code:`CHOICES()`
function that returns a :code:`None` value.

.. code-block:: python

    def CHOICES(ind):
        
        return None

If multiple-choice answers are provided, the :code:`CHOICES()` function should
return a dictionary containing the key :code:`choices`. The value of this key
should be a list containing the correct answer and wrong answers. In other
words,it should include everything that is to be listed as answer choices in the
question. An example of using the :code:`choices` key-value pair is shown below.

.. code-block:: python

    import teepy
    
    def CHOICES(ind):
        choices = teepy.get_answers(PROBLEM(ind))
        
        choices.extend(['Red',
                        'Green',
                        'Yellow',
                        'Orange'])
        
        random.shuffle(choices)
        
        return {'choices': choices}

The example above also illustrates the use of a TEEPy function called
:code:`get_answers()`. The function takes one argument of a :code:`PROBLEMS()`
function with the particular index value that is to used. The function always
returns a list even if the answer to the problem is a single value answer. The
example above also demonstrates the use of Python's built-in module
:code:`random`. :code:`random` has many useful methods but the one here shuffles
a list. The list of choices does not have to be rearranged. An example of not
mixing the list of options is shown below.

.. code-block:: python

    import teepy
    
    def CHOICES(ind):
        choices = ['1', '2']
        choices.extend(teepy.get_answers(PROBLEM(ind)))
        
        return {'choices': choices}

There are a couple of things worth mentioning about the  :code:`CHOICES()`
function when an answer has units. When an answer has units, TEEPy has the
function :code:`generate_choices()` available to generate randomized choices.
The function takes three arguments; the number of choices, the correct answer,
and the step size between choices. The :code:`CHOICES()` function must also have
a key :code:`choice_format` in the dictionary it returns. The value of this key
is the desired format type of the answer choices. An example of using the
:code:`generate_choices()` function and the :code:`choice_format` key is shown
below.

.. code-block:: python

    import teepy
    
    def CHOICES(ind):
        N = 10
        choice_format = '{:0.3f}'
        step = random.uniform(0.01, 0.05)
        ans = teepy.get_answers(PROBLEM(ind))
        
        choices = teepy.generate_choices(N, ans, step)
        
        return {'choices': choices, 'choice_format': choice_format}

All of the examples seen above may be found in the examples directory.

Assessment Creator (AC)
-----------------------

Work in progress

.. _`LaTeX`: https://en.wikipedia.org/wiki/LaTeX
.. _`MathJax`: https://www.mathjax.org/
.. _`pint`: https://github.com/hgrecco/pint