Robotframework-seleniumtestability
============================

Extension library for SeleniumLibrary that provides either manual or automatic
waiting asyncronous events within SUT.

This is accomplished by utilizing following 2 libraries. First one provides an
API and second one provides bindings.

 * https://github.com/alfonso-presa/testability.js
 * https://github.com/alfonso-presa/testability-browser-bindings


# Installation

```
pip install robotframework-seleniumtestability
```

# How things work ?

System under test needs to be instrumented before asyncronous events can be
detected and acted upon. Instrumentation can be multiple ways:

1. SUT or its build tooling need to inject the javascript files into itself
   and then finally call "instrumentBrowser()" function in window scope
2. SUT could be instrumented by MITM proxy that takes care of injecting the
   required javascript files into the page and then calling the
   instrumentBrowser() function in window scope.
3. If either of above options is not possible, you can call `Inject
   Testability` keyword and then `Instrument Browser'

Benefit of first and second option is that testability api is initialized the
same time as your SUT. If the application initialization triggers any
asyncronous actions, these are already being detected and there's no need for
waiting in the begining for a good state when your testing script can start.

# Usage

## Initialize library

```
Library         SeleniumTestability     wait_testability=False
```

If `wait_testability`is set to true, just before a selenium library keyword is
executed, SeleniumTestability library will wait until testability.js api call
returns. If the value is set to false, user needs to call `Wait For
Testability Ready` keyword.

You can pass any parameters that SeleniumLibrary accepts also to
SeleniumTestability.

## Instrumenting the browser.

In "How things work ?"_ section, we are describing ways how the SUT should be
instrumented. Scenarios 1 & 2 are not covered by this documentation. Scenario
3 goes as follows:

```
  Inject Testability
  Instrument Browser
```

## Waiting

If SeleniumTestability library was initialized with wait_testability set to
False, user / testscripts will need to explicitly call `Wait For Testability
Ready` keyword. Example:

```
  Click Element   id:button_that_triggers_ajax_request
  Wait For Testability Ready
  Click Element   id:some_other_element
```

In this case, Wait For Testability Ready will wait until the ajax request has
finished its operation and only then it will pass the execution to the next
keyword.

However, if SeleniumTestability was initialized with wait_testability set to
True, Wait For Testability Ready keyword can be omitted. Do note: waiting
happens only for keywords that directly try to access the browser in ways that
a asyncronous action within the SUT could affect the result of the keyword.


# Current Features

* Can detect setTimeout & setImmediate calls and wait for them.
* Can detect fetch() call and wait for it to finish
* Can detect XHR requests and wait for them to finish
* Can detect CSS Animations and wait form them to finish
* Can detect CSS Transitions and wait form them to finish

Do note that CSS animations and transitions do not work properly in Chrome.

# TODO:

* Support ES6 Promises
* Investigate on possibility of polyfilling css animations and transitions in
  Chrome.
* Addon possibility to for bindings. For example, one might want to extend the
  functionality to support asyncronous actions of any web framework (like
  Angular, React and what not)
