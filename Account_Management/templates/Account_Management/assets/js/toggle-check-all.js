/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "/";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 34);
/******/ })
/************************************************************************/
/******/ ({

/***/ "./node_modules/@babel/runtime/helpers/typeof.js":
/*!*******************************************************!*\
  !*** ./node_modules/@babel/runtime/helpers/typeof.js ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

function _typeof(obj) {
  "@babel/helpers - typeof";

  if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") {
    module.exports = _typeof = function _typeof(obj) {
      return typeof obj;
    };
  } else {
    module.exports = _typeof = function _typeof(obj) {
      return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj;
    };
  }

  return _typeof(obj);
}

module.exports = _typeof;

/***/ }),

/***/ "./src/js/toggle-check-all.js":
/*!************************************!*\
  !*** ./src/js/toggle-check-all.js ***!
  \************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var _typeof = __webpack_require__(/*! @babel/runtime/helpers/typeof */ "./node_modules/@babel/runtime/helpers/typeof.js");

var toggleCheckAllComponent = function toggleCheckAllComponent() {
  return {
    properties: {
      target: {
        reflectToAttribute: true
      }
    },
    listeners: ['_onClick(click)'],

    /**
     * Fire a DOM Event on the HTMLElement
     * @param  {String} eventName The event name
     */
    dispatchEvent: function dispatchEvent(eventName, element) {
      var event;
      var bubbles = false;

      if ('CustomEvent' in window && _typeof(window.CustomEvent) === 'object') {
        try {
          event = new CustomEvent(eventName, {
            bubbles: bubbles,
            cancelable: false
          });
        } catch (e) {
          event = new this.CustomEvent_(eventName, {
            bubbles: bubbles,
            cancelable: false
          });
        }
      } else {
        event = document.createEvent('Event');
        event.initEvent(eventName, bubbles, true);
      }

      element.dispatchEvent(event);
    },
    CustomEvent_: function CustomEvent_(event, params) {
      params = params || {
        bubbles: false,
        cancelable: false,
        detail: undefined
      };
      var evt = document.createEvent('CustomEvent');
      evt.initCustomEvent(event, params.bubbles, params.cancelable, params.detail);
      return evt;
    },

    get $target() {
      return document.querySelector(this.target);
    },

    get $targets() {
      return this.$target.querySelectorAll('[type="checkbox"]');
    },

    _onClick: function _onClick(e) {
      var _this = this;

      if (this.element.type && this.element.type === 'checkbox') {
        this._checked = this.element.checked;
      } else {
        this._checked = !this._checked;
        e.preventDefault();
      }

      this.$targets.forEach(function (i) {
        i.checked = _this._checked;

        _this.dispatchEvent('change', i);
      });
    }
  };
};

domFactory.handler.register('toggle-check-all', toggleCheckAllComponent);

/***/ }),

/***/ 34:
/*!******************************************!*\
  !*** multi ./src/js/toggle-check-all.js ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /Users/demi/Documents/GitHub/admin-educate/src/js/toggle-check-all.js */"./src/js/toggle-check-all.js");


/***/ })

/******/ });
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vd2VicGFjay9ib290c3RyYXAiLCJ3ZWJwYWNrOi8vLy4vbm9kZV9tb2R1bGVzL0BiYWJlbC9ydW50aW1lL2hlbHBlcnMvdHlwZW9mLmpzIiwid2VicGFjazovLy8uL3NyYy9qcy90b2dnbGUtY2hlY2stYWxsLmpzIl0sIm5hbWVzIjpbInRvZ2dsZUNoZWNrQWxsQ29tcG9uZW50IiwicHJvcGVydGllcyIsInRhcmdldCIsInJlZmxlY3RUb0F0dHJpYnV0ZSIsImxpc3RlbmVycyIsImRpc3BhdGNoRXZlbnQiLCJidWJibGVzIiwid2luZG93IiwiZXZlbnQiLCJjYW5jZWxhYmxlIiwiZG9jdW1lbnQiLCJlbGVtZW50IiwiQ3VzdG9tRXZlbnRfIiwicGFyYW1zIiwiZGV0YWlsIiwidW5kZWZpbmVkIiwiZXZ0IiwiX29uQ2xpY2siLCJlIiwiaSIsImRvbUZhY3RvcnkiXSwibWFwcGluZ3MiOiI7UUFBQTtRQUNBOztRQUVBO1FBQ0E7O1FBRUE7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7O1FBRUE7UUFDQTs7UUFFQTtRQUNBOztRQUVBO1FBQ0E7UUFDQTs7O1FBR0E7UUFDQTs7UUFFQTtRQUNBOztRQUVBO1FBQ0E7UUFDQTtRQUNBLDBDQUEwQyxnQ0FBZ0M7UUFDMUU7UUFDQTs7UUFFQTtRQUNBO1FBQ0E7UUFDQSx3REFBd0Qsa0JBQWtCO1FBQzFFO1FBQ0EsaURBQWlELGNBQWM7UUFDL0Q7O1FBRUE7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBLHlDQUF5QyxpQ0FBaUM7UUFDMUUsZ0hBQWdILG1CQUFtQixFQUFFO1FBQ3JJO1FBQ0E7O1FBRUE7UUFDQTtRQUNBO1FBQ0EsMkJBQTJCLDBCQUEwQixFQUFFO1FBQ3ZELGlDQUFpQyxlQUFlO1FBQ2hEO1FBQ0E7UUFDQTs7UUFFQTtRQUNBLHNEQUFzRCwrREFBK0Q7O1FBRXJIO1FBQ0E7OztRQUdBO1FBQ0E7Ozs7Ozs7Ozs7OztBQ2xGQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsR0FBRztBQUNIO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUEseUI7Ozs7Ozs7Ozs7Ozs7QUNoQkEsSUFBTUEsdUJBQXVCLEdBQUcsU0FBMUJBLHVCQUEwQjtBQUFBLFNBQU87QUFDckNDLGNBQVUsRUFBRTtBQUNWQyxZQUFNLEVBQUU7QUFDTkMsMEJBQWtCLEVBQUU7QUFEZDtBQURFLEtBRHlCO0FBT3JDQyxhQUFTLEVBQUUsQ0FQMEIsaUJBTzFCLENBUDBCOztBQVdyQzs7OztBQUlBQyxpQkFmcUMsNkNBZUY7QUFDakM7QUFDQSxVQUFJQyxPQUFPLEdBQVg7O0FBQ0EsVUFBSSwyQkFBMkIsUUFBT0MsTUFBTSxDQUFiLGlCQUEvQixVQUF1RTtBQUNyRSxZQUFJO0FBQ0ZDLGVBQUssR0FBRywyQkFBMkI7QUFDakNGLG1CQUFPLEVBRDBCO0FBRWpDRyxzQkFBVSxFQUFFO0FBRnFCLFdBQTNCLENBQVJEO0FBREYsVUFNQSxVQUFVO0FBQ1JBLGVBQUssR0FBRyxJQUFJLEtBQUosd0JBQWlDO0FBQ3ZDRixtQkFBTyxFQURnQztBQUV2Q0csc0JBQVUsRUFBRTtBQUYyQixXQUFqQyxDQUFSRDtBQUlEO0FBWkgsYUFjSztBQUNIQSxhQUFLLEdBQUdFLFFBQVEsQ0FBUkEsWUFBUkYsT0FBUUUsQ0FBUkY7QUFDQUEsYUFBSyxDQUFMQTtBQUNEOztBQUNERyxhQUFPLENBQVBBO0FBcENtQztBQXVDckNDLGdCQXZDcUMsdUNBdUNSO0FBQzNCQyxZQUFNLEdBQUdBLE1BQU0sSUFBSTtBQUFFUCxlQUFPLEVBQVQ7QUFBa0JHLGtCQUFVLEVBQTVCO0FBQXFDSyxjQUFNLEVBQUVDO0FBQTdDLE9BQW5CRjtBQUNBLFVBQUlHLEdBQUcsR0FBR04sUUFBUSxDQUFSQSxZQUFWLGFBQVVBLENBQVY7QUFDQU0sU0FBRyxDQUFIQSx1QkFBMkJILE1BQU0sQ0FBakNHLFNBQTJDSCxNQUFNLENBQWpERyxZQUE4REgsTUFBTSxDQUFwRUc7QUFDQTtBQTNDbUM7O0FBOENyQyxrQkFBZTtBQUNiLGFBQU9OLFFBQVEsQ0FBUkEsY0FBdUIsS0FBOUIsTUFBT0EsQ0FBUDtBQS9DbUM7O0FBa0RyQyxtQkFBZ0I7QUFDZCxhQUFPLDhCQUFQLG1CQUFPLENBQVA7QUFuRG1DOztBQXNEckNPLFlBdERxQyx1QkFzRHhCO0FBQUE7O0FBQ1gsVUFBSSxxQkFBcUIsc0JBQXpCLFlBQTJEO0FBQ3pELHdCQUFnQixhQUFoQjtBQURGLGFBR0s7QUFDSCx3QkFBZ0IsQ0FBQyxLQUFqQjtBQUNBQyxTQUFDLENBQURBO0FBQ0Q7O0FBRUQsNEJBQXNCLGFBQUs7QUFDekJDLFNBQUMsQ0FBREEsVUFBWSxLQUFJLENBQWhCQTs7QUFDQSxhQUFJLENBQUo7QUFGRjtBQUlEO0FBbkVvQyxHQUFQO0FBQWhDOztBQXNFQUMsVUFBVSxDQUFWQSw4RCIsImZpbGUiOiIvZGlzdC9hc3NldHMvanMvdG9nZ2xlLWNoZWNrLWFsbC5qcyIsInNvdXJjZXNDb250ZW50IjpbIiBcdC8vIFRoZSBtb2R1bGUgY2FjaGVcbiBcdHZhciBpbnN0YWxsZWRNb2R1bGVzID0ge307XG5cbiBcdC8vIFRoZSByZXF1aXJlIGZ1bmN0aW9uXG4gXHRmdW5jdGlvbiBfX3dlYnBhY2tfcmVxdWlyZV9fKG1vZHVsZUlkKSB7XG5cbiBcdFx0Ly8gQ2hlY2sgaWYgbW9kdWxlIGlzIGluIGNhY2hlXG4gXHRcdGlmKGluc3RhbGxlZE1vZHVsZXNbbW9kdWxlSWRdKSB7XG4gXHRcdFx0cmV0dXJuIGluc3RhbGxlZE1vZHVsZXNbbW9kdWxlSWRdLmV4cG9ydHM7XG4gXHRcdH1cbiBcdFx0Ly8gQ3JlYXRlIGEgbmV3IG1vZHVsZSAoYW5kIHB1dCBpdCBpbnRvIHRoZSBjYWNoZSlcbiBcdFx0dmFyIG1vZHVsZSA9IGluc3RhbGxlZE1vZHVsZXNbbW9kdWxlSWRdID0ge1xuIFx0XHRcdGk6IG1vZHVsZUlkLFxuIFx0XHRcdGw6IGZhbHNlLFxuIFx0XHRcdGV4cG9ydHM6IHt9XG4gXHRcdH07XG5cbiBcdFx0Ly8gRXhlY3V0ZSB0aGUgbW9kdWxlIGZ1bmN0aW9uXG4gXHRcdG1vZHVsZXNbbW9kdWxlSWRdLmNhbGwobW9kdWxlLmV4cG9ydHMsIG1vZHVsZSwgbW9kdWxlLmV4cG9ydHMsIF9fd2VicGFja19yZXF1aXJlX18pO1xuXG4gXHRcdC8vIEZsYWcgdGhlIG1vZHVsZSBhcyBsb2FkZWRcbiBcdFx0bW9kdWxlLmwgPSB0cnVlO1xuXG4gXHRcdC8vIFJldHVybiB0aGUgZXhwb3J0cyBvZiB0aGUgbW9kdWxlXG4gXHRcdHJldHVybiBtb2R1bGUuZXhwb3J0cztcbiBcdH1cblxuXG4gXHQvLyBleHBvc2UgdGhlIG1vZHVsZXMgb2JqZWN0IChfX3dlYnBhY2tfbW9kdWxlc19fKVxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5tID0gbW9kdWxlcztcblxuIFx0Ly8gZXhwb3NlIHRoZSBtb2R1bGUgY2FjaGVcbiBcdF9fd2VicGFja19yZXF1aXJlX18uYyA9IGluc3RhbGxlZE1vZHVsZXM7XG5cbiBcdC8vIGRlZmluZSBnZXR0ZXIgZnVuY3Rpb24gZm9yIGhhcm1vbnkgZXhwb3J0c1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5kID0gZnVuY3Rpb24oZXhwb3J0cywgbmFtZSwgZ2V0dGVyKSB7XG4gXHRcdGlmKCFfX3dlYnBhY2tfcmVxdWlyZV9fLm8oZXhwb3J0cywgbmFtZSkpIHtcbiBcdFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgbmFtZSwgeyBlbnVtZXJhYmxlOiB0cnVlLCBnZXQ6IGdldHRlciB9KTtcbiBcdFx0fVxuIFx0fTtcblxuIFx0Ly8gZGVmaW5lIF9fZXNNb2R1bGUgb24gZXhwb3J0c1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5yID0gZnVuY3Rpb24oZXhwb3J0cykge1xuIFx0XHRpZih0eXBlb2YgU3ltYm9sICE9PSAndW5kZWZpbmVkJyAmJiBTeW1ib2wudG9TdHJpbmdUYWcpIHtcbiBcdFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgU3ltYm9sLnRvU3RyaW5nVGFnLCB7IHZhbHVlOiAnTW9kdWxlJyB9KTtcbiBcdFx0fVxuIFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgJ19fZXNNb2R1bGUnLCB7IHZhbHVlOiB0cnVlIH0pO1xuIFx0fTtcblxuIFx0Ly8gY3JlYXRlIGEgZmFrZSBuYW1lc3BhY2Ugb2JqZWN0XG4gXHQvLyBtb2RlICYgMTogdmFsdWUgaXMgYSBtb2R1bGUgaWQsIHJlcXVpcmUgaXRcbiBcdC8vIG1vZGUgJiAyOiBtZXJnZSBhbGwgcHJvcGVydGllcyBvZiB2YWx1ZSBpbnRvIHRoZSBuc1xuIFx0Ly8gbW9kZSAmIDQ6IHJldHVybiB2YWx1ZSB3aGVuIGFscmVhZHkgbnMgb2JqZWN0XG4gXHQvLyBtb2RlICYgOHwxOiBiZWhhdmUgbGlrZSByZXF1aXJlXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLnQgPSBmdW5jdGlvbih2YWx1ZSwgbW9kZSkge1xuIFx0XHRpZihtb2RlICYgMSkgdmFsdWUgPSBfX3dlYnBhY2tfcmVxdWlyZV9fKHZhbHVlKTtcbiBcdFx0aWYobW9kZSAmIDgpIHJldHVybiB2YWx1ZTtcbiBcdFx0aWYoKG1vZGUgJiA0KSAmJiB0eXBlb2YgdmFsdWUgPT09ICdvYmplY3QnICYmIHZhbHVlICYmIHZhbHVlLl9fZXNNb2R1bGUpIHJldHVybiB2YWx1ZTtcbiBcdFx0dmFyIG5zID0gT2JqZWN0LmNyZWF0ZShudWxsKTtcbiBcdFx0X193ZWJwYWNrX3JlcXVpcmVfXy5yKG5zKTtcbiBcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KG5zLCAnZGVmYXVsdCcsIHsgZW51bWVyYWJsZTogdHJ1ZSwgdmFsdWU6IHZhbHVlIH0pO1xuIFx0XHRpZihtb2RlICYgMiAmJiB0eXBlb2YgdmFsdWUgIT0gJ3N0cmluZycpIGZvcih2YXIga2V5IGluIHZhbHVlKSBfX3dlYnBhY2tfcmVxdWlyZV9fLmQobnMsIGtleSwgZnVuY3Rpb24oa2V5KSB7IHJldHVybiB2YWx1ZVtrZXldOyB9LmJpbmQobnVsbCwga2V5KSk7XG4gXHRcdHJldHVybiBucztcbiBcdH07XG5cbiBcdC8vIGdldERlZmF1bHRFeHBvcnQgZnVuY3Rpb24gZm9yIGNvbXBhdGliaWxpdHkgd2l0aCBub24taGFybW9ueSBtb2R1bGVzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLm4gPSBmdW5jdGlvbihtb2R1bGUpIHtcbiBcdFx0dmFyIGdldHRlciA9IG1vZHVsZSAmJiBtb2R1bGUuX19lc01vZHVsZSA/XG4gXHRcdFx0ZnVuY3Rpb24gZ2V0RGVmYXVsdCgpIHsgcmV0dXJuIG1vZHVsZVsnZGVmYXVsdCddOyB9IDpcbiBcdFx0XHRmdW5jdGlvbiBnZXRNb2R1bGVFeHBvcnRzKCkgeyByZXR1cm4gbW9kdWxlOyB9O1xuIFx0XHRfX3dlYnBhY2tfcmVxdWlyZV9fLmQoZ2V0dGVyLCAnYScsIGdldHRlcik7XG4gXHRcdHJldHVybiBnZXR0ZXI7XG4gXHR9O1xuXG4gXHQvLyBPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGxcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubyA9IGZ1bmN0aW9uKG9iamVjdCwgcHJvcGVydHkpIHsgcmV0dXJuIE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbChvYmplY3QsIHByb3BlcnR5KTsgfTtcblxuIFx0Ly8gX193ZWJwYWNrX3B1YmxpY19wYXRoX19cbiBcdF9fd2VicGFja19yZXF1aXJlX18ucCA9IFwiL1wiO1xuXG5cbiBcdC8vIExvYWQgZW50cnkgbW9kdWxlIGFuZCByZXR1cm4gZXhwb3J0c1xuIFx0cmV0dXJuIF9fd2VicGFja19yZXF1aXJlX18oX193ZWJwYWNrX3JlcXVpcmVfXy5zID0gMzQpO1xuIiwiZnVuY3Rpb24gX3R5cGVvZihvYmopIHtcbiAgXCJAYmFiZWwvaGVscGVycyAtIHR5cGVvZlwiO1xuXG4gIGlmICh0eXBlb2YgU3ltYm9sID09PSBcImZ1bmN0aW9uXCIgJiYgdHlwZW9mIFN5bWJvbC5pdGVyYXRvciA9PT0gXCJzeW1ib2xcIikge1xuICAgIG1vZHVsZS5leHBvcnRzID0gX3R5cGVvZiA9IGZ1bmN0aW9uIF90eXBlb2Yob2JqKSB7XG4gICAgICByZXR1cm4gdHlwZW9mIG9iajtcbiAgICB9O1xuICB9IGVsc2Uge1xuICAgIG1vZHVsZS5leHBvcnRzID0gX3R5cGVvZiA9IGZ1bmN0aW9uIF90eXBlb2Yob2JqKSB7XG4gICAgICByZXR1cm4gb2JqICYmIHR5cGVvZiBTeW1ib2wgPT09IFwiZnVuY3Rpb25cIiAmJiBvYmouY29uc3RydWN0b3IgPT09IFN5bWJvbCAmJiBvYmogIT09IFN5bWJvbC5wcm90b3R5cGUgPyBcInN5bWJvbFwiIDogdHlwZW9mIG9iajtcbiAgICB9O1xuICB9XG5cbiAgcmV0dXJuIF90eXBlb2Yob2JqKTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBfdHlwZW9mOyIsImNvbnN0IHRvZ2dsZUNoZWNrQWxsQ29tcG9uZW50ID0gKCkgPT4gKHtcbiAgcHJvcGVydGllczoge1xuICAgIHRhcmdldDoge1xuICAgICAgcmVmbGVjdFRvQXR0cmlidXRlOiB0cnVlXG4gICAgfSxcbiAgfSxcblxuICBsaXN0ZW5lcnM6IFtcbiAgICAnX29uQ2xpY2soY2xpY2spJyxcbiAgXSxcblxuICAvKipcbiAgICogRmlyZSBhIERPTSBFdmVudCBvbiB0aGUgSFRNTEVsZW1lbnRcbiAgICogQHBhcmFtICB7U3RyaW5nfSBldmVudE5hbWUgVGhlIGV2ZW50IG5hbWVcbiAgICovXG4gIGRpc3BhdGNoRXZlbnQgKGV2ZW50TmFtZSwgZWxlbWVudCkge1xuICAgIGxldCBldmVudFxuICAgIGxldCBidWJibGVzID0gZmFsc2VcbiAgICBpZiAoJ0N1c3RvbUV2ZW50JyBpbiB3aW5kb3cgJiYgdHlwZW9mIHdpbmRvdy5DdXN0b21FdmVudCA9PT0gJ29iamVjdCcpIHtcbiAgICAgIHRyeSB7XG4gICAgICAgIGV2ZW50ID0gbmV3IEN1c3RvbUV2ZW50KGV2ZW50TmFtZSwge1xuICAgICAgICAgIGJ1YmJsZXMsXG4gICAgICAgICAgY2FuY2VsYWJsZTogZmFsc2VcbiAgICAgICAgfSkgXG4gICAgICB9IFxuICAgICAgY2F0Y2ggKGUpIHtcbiAgICAgICAgZXZlbnQgPSBuZXcgdGhpcy5DdXN0b21FdmVudF8oZXZlbnROYW1lLCB7XG4gICAgICAgICAgYnViYmxlcyxcbiAgICAgICAgICBjYW5jZWxhYmxlOiBmYWxzZVxuICAgICAgICB9KVxuICAgICAgfVxuICAgIH1cbiAgICBlbHNlIHtcbiAgICAgIGV2ZW50ID0gZG9jdW1lbnQuY3JlYXRlRXZlbnQoJ0V2ZW50JylcbiAgICAgIGV2ZW50LmluaXRFdmVudChldmVudE5hbWUsIGJ1YmJsZXMsIHRydWUpXG4gICAgfVxuICAgIGVsZW1lbnQuZGlzcGF0Y2hFdmVudChldmVudClcbiAgfSxcblxuICBDdXN0b21FdmVudF8gKGV2ZW50LCBwYXJhbXMpIHtcbiAgICBwYXJhbXMgPSBwYXJhbXMgfHwgeyBidWJibGVzOiBmYWxzZSwgY2FuY2VsYWJsZTogZmFsc2UsIGRldGFpbDogdW5kZWZpbmVkIH1cbiAgICB2YXIgZXZ0ID0gZG9jdW1lbnQuY3JlYXRlRXZlbnQoJ0N1c3RvbUV2ZW50JylcbiAgICBldnQuaW5pdEN1c3RvbUV2ZW50KGV2ZW50LCBwYXJhbXMuYnViYmxlcywgcGFyYW1zLmNhbmNlbGFibGUsIHBhcmFtcy5kZXRhaWwpXG4gICAgcmV0dXJuIGV2dFxuICB9LFxuXG4gIGdldCAkdGFyZ2V0ICgpIHtcbiAgICByZXR1cm4gZG9jdW1lbnQucXVlcnlTZWxlY3Rvcih0aGlzLnRhcmdldClcbiAgfSxcblxuICBnZXQgJHRhcmdldHMgKCkge1xuICAgIHJldHVybiB0aGlzLiR0YXJnZXQucXVlcnlTZWxlY3RvckFsbCgnW3R5cGU9XCJjaGVja2JveFwiXScpXG4gIH0sXG5cbiAgX29uQ2xpY2sgKGUpIHtcbiAgICBpZiAodGhpcy5lbGVtZW50LnR5cGUgJiYgdGhpcy5lbGVtZW50LnR5cGUgPT09ICdjaGVja2JveCcpIHtcbiAgICAgIHRoaXMuX2NoZWNrZWQgPSB0aGlzLmVsZW1lbnQuY2hlY2tlZFxuICAgIH1cbiAgICBlbHNlIHtcbiAgICAgIHRoaXMuX2NoZWNrZWQgPSAhdGhpcy5fY2hlY2tlZFxuICAgICAgZS5wcmV2ZW50RGVmYXVsdCgpXG4gICAgfVxuXG4gICAgdGhpcy4kdGFyZ2V0cy5mb3JFYWNoKGkgPT4ge1xuICAgICAgaS5jaGVja2VkID0gdGhpcy5fY2hlY2tlZFxuICAgICAgdGhpcy5kaXNwYXRjaEV2ZW50KCdjaGFuZ2UnLCBpKVxuICAgIH0pXG4gIH1cbn0pXG5cbmRvbUZhY3RvcnkuaGFuZGxlci5yZWdpc3RlcigndG9nZ2xlLWNoZWNrLWFsbCcsIHRvZ2dsZUNoZWNrQWxsQ29tcG9uZW50KSJdLCJzb3VyY2VSb290IjoiIn0=