**************************************
Welcome to cocotb-bus's documentation!
**************************************

..
   This documentation tries to follow https://www.divio.com/blog/documentation/ (Daniele Procida)
   Other media about the same topic:
   - https://ep2018.europython.eu/media/conference/slides/get-your-documentation-right.pdf
   - https://www.youtube.com/watch?v=t4vKPhjcMZg
   - A good example: http://docs.django-cms.org/en/latest/contributing/documentation.html#contributing-documentation

   See also https://github.com/cocotb/cocotb/wiki/Howto:-Writing-Documentation

What is cocotb-bus?
===================

**cocotb-bus** consists of pre-packaged testbenching tools and reusable bus interfaces
for https://cocotb.org.

A bit more detailed, cocotb-bus is:

* A set of Driver & Monitor base classes to assist in creating cocotb VIPs.
* An implementation of a scoreboard class for cocotb.
* Sample implementation of protocol bus drivers using these classes.

Dependencies
------------

In addition to what cocotb itself requires,
cocotb-bus has a dependency on ``scapy`` (https://scapy.readthedocs.io/)
for its :func:`scapy.utils.hexdump` and :func:`scapy.utils.hexdiff` functions
used in the :mod:`.scoreboard`.


.. toctree::
   :maxdepth: 1
   :hidden:

   testbench_tools

..
   install
   quickstart
   Tutorials - lessons that take the reader by the hand through a series of steps to complete a project
   (Example: kid cooking; learning-oriented)

   - learning by doing
   - getting started
   - inspiring confidence
   - repeatability
   - immediate sense of achievement
   - concreteness, not abstraction
   - minimum necessary explanation
   - no distractions

..
   .. toctree::
      :maxdepth: 1
      :caption: Tutorials
      :name: tutorials
      :hidden:

      examples


..
   How-To Guides - guides that take the reader through the steps required to solve a common problem
   (Example: recipe; problem-oriented)

   - a series of steps
   - a focus on the goal
   - addressing a specific question
   - no unnecessary explanation
   - a little flexibility
   - practical usability
   - good naming

..
   .. toctree::
      :maxdepth: 1
      :caption: How-to Guides
      :name: howto_guides
      :hidden:

      writing_testbenches
      runner
      coroutines
      triggers
      custom_flows
      rotating_logger

.. todo::
   - Howto use the baseclasses to create VIP
   - Roadmap


..
   Explanation (Background, Discussions) - discussions that clarify and illuminate a particular topic
   (Example: history of cooking; understanding-oriented)

   - giving context
   - explaining why
   - multiple examples, alternative approaches
   - making connections
   - no instruction or technical description

..
   .. toctree::
      :maxdepth: 1
      :caption: Key topics
      :name: key_topics
      :hidden:

      install_devel
      troubleshooting



..
   Reference - technical descriptions of the machinery and its operation
   (Example: Wikipedia pages of ingredients; information-oriented)

   - structure
   - consistency
   - description
   - accuracy

..
.. toctree::
   :maxdepth: 1
   :caption: Reference
   :name: reference
   :hidden:

   Python Code Library Reference <library_reference>

.. toctree::
   :maxdepth: 1
   :caption: Development & Community
   :name: development_community
   :hidden:

   release_notes
..
      roadmap
      contributors
      further_resources

.. todo::
   - Add "Join us online" and "Contributing"
   - In Contributing, add explanation on how to provide a PR, how to test existing PRs, etc.
   - merge `further_resources` into Contributing

.. toctree::
   :maxdepth: 1
   :caption: Index
   :name: index
   :hidden:

   Classes, Methods, Variables etc. <genindex>
   glossary
..
   Python Modules <py-modindex>
