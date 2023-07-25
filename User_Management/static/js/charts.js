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
/******/ 	return __webpack_require__(__webpack_require__.s = 14);
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

/***/ "./src/js/plugins/charts.js":
/*!**********************************!*\
  !*** ./src/js/plugins/charts.js ***!
  \**********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var _typeof = __webpack_require__(/*! @babel/runtime/helpers/typeof */ "./node_modules/@babel/runtime/helpers/typeof.js");

var extend = function extend(object, value) {
  for (var key in value) {
    "object" != _typeof(value[key]) ? object[key] = value[key] : extend(object[key], value[key]);
  }
};

var add = function add(element) {
  var data = element.data("add");
  var chart = $(element.data("target")).data("chart");

  if (element.is(":checked")) {
    var addRecursive = function addRecursive(chart, data) {
      for (var o in data) {
        Array.isArray(data[o]) ? data[o].forEach(function (a) {
          chart[o].push(a);
        }) : addRecursive(chart[o], data[o]);
      }
    };

    addRecursive(chart, data);
  } else {
    var removeRecursive = function removeRecursive(chart, data) {
      for (var o in data) {
        Array.isArray(data[o]) ? data[o].forEach(function (a) {
          chart[o].pop();
        }) : removeRecursive(chart[o], data[o]);
      }
    };

    removeRecursive(chart, data);
  }

  chart.update();
};

var update = function update(element) {
  var data = element.data("update");
  var chart = $(element.data("target")).data("chart");
  extend(chart, data);

  if (void 0 !== element.data("prefix") || void 0 !== element.data("suffix")) {
    var prefix = element.data("prefix") ? element.data("prefix") : "";
    var suffix = element.data("suffix") ? element.data("suffix") : "";

    if (chart.options.scales !== undefined) {
      chart.options.scales.yAxes[0].ticks.callback = function (a) {
        if (!(a % 10)) return prefix + a + suffix;
      };
    }

    chart.options.tooltips.callbacks.label = function (a, e) {
      var t = e.datasets[a.datasetIndex].label || "",
          o = a.yLabel || e.datasets[0].data[a.index],
          r = "";
      return 1 < e.datasets.length && (r += '<span class="popover-body-label mr-auto">' + t + "</span>"), r += '<span class="popover-body-value">' + prefix + o + suffix + "</span>";
    };
  }

  chart.update();
};

var globalSettings = {
  responsive: true,
  maintainAspectRatio: false,
  defaultColor: "dark" == settings.charts.colorScheme ? settings.colors.gray[700] : settings.colors.gray[600],
  defaultFontColor: "dark" == settings.charts.colorScheme ? settings.colors.gray[700] : settings.colors.gray[600],
  defaultFontFamily: settings.fonts.base,
  defaultFontSize: 13,
  layout: {
    padding: 0
  },
  legend: {
    display: false,
    position: "bottom",
    labels: {
      usePointStyle: true,
      padding: 16
    }
  },
  elements: {
    point: {
      radius: 0,
      backgroundColor: settings.colors.primary[500]
    },
    line: {
      tension: .4,
      borderWidth: 3,
      borderColor: settings.colors.primary[500],
      backgroundColor: settings.colors.transparent,
      borderCapStyle: "rounded"
    },
    rectangle: {
      backgroundColor: settings.colors.primary[500]
    },
    arc: {
      backgroundColor: settings.colors.primary[500],
      borderColor: "dark" == settings.charts.colorScheme ? settings.colors.gray[800] : settings.colors.white,
      borderWidth: 4
    }
  },
  tooltips: {
    enabled: !1,
    mode: "index",
    intersect: !1,
    custom: function custom(r) {
      var a = $("#chart-tooltip");

      if (a.length || (a = $('<div id="chart-tooltip" class="popover bs-popover-top" role="tooltip"></div>'), $("body").append(a)), 0 !== r.opacity) {
        if (r.body) {
          var e = r.title || [],
              l = r.body.map(function (a) {
            return a.lines;
          }),
              n = "";
          n += '<div class="arrow"></div>', e.forEach(function (a) {
            n += '<h3 class="popover-header text-center">' + a + "</h3>";
          }), l.forEach(function (a, e) {
            var t = '<span class="popover-body-indicator" style="background-color: ' + r.labelColors[e].backgroundColor + '"></span>',
                o = 1 < l.length ? "justify-content-left" : "justify-content-center";
            n += '<div class="popover-body d-flex align-items-center ' + o + '">' + t + a + "</div>";
          }), a.html(n);
        }

        var t = $(this._chart.canvas),
            o = (t.outerWidth(), t.outerHeight(), t.offset().top),
            s = t.offset().left,
            i = a.outerWidth(),
            c = a.outerHeight(),
            d = o + r.caretY - c - 16,
            u = s + r.caretX - i / 2;
        a.css({
          top: d + "px",
          left: u + "px",
          display: "block"
        });
      } else a.css("display", "none");
    },
    callbacks: {
      label: function label(a, e) {
        var t = e.datasets[a.datasetIndex].label || "",
            o = a.yLabel,
            r = "";
        return 1 < e.datasets.length && (r += '<span class="popover-body-label mr-auto">' + t + "</span>"), r += '<span class="popover-body-value">' + o + "</span>";
      }
    }
  }
};
var doughnutSettings = {
  cutoutPercentage: 83,
  tooltips: {
    callbacks: {
      title: function title(a, e) {
        return e.labels[a[0].index];
      },
      label: function label(a, e) {
        var t = "";
        return t += '<span class="popover-body-value">' + e.datasets[0].data[a.index] + "</span>";
      }
    }
  },
  legendCallback: function legendCallback(a) {
    var o = a.data,
        r = "";
    return o.labels.forEach(function (a, e) {
      var t = o.datasets[0].backgroundColor[e];
      r += '<span class="chart-legend-item">', r += '<i class="chart-legend-indicator" style="background-color: ' + t + '"></i>', r += a, r += "</span>";
    }), r;
  }
};

var create = function create(id) {
  var type = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 'line';
  var options = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};
  var data = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : {};
  var element = $(id);
  var chart = new Chart(element, {
    type: type,
    options: options,
    data: data
  });
  element.data("chart", chart);

  if (element.data("chart-legend")) {
    document.querySelector(element.data("chart-legend")).innerHTML = chart.generateLegend();
  }
};

var init = function init() {
  extend(Chart, {
    defaults: {
      global: globalSettings,
      doughnut: doughnutSettings
    }
  });
  Chart.scaleService.updateScaleDefaults("linear", {
    gridLines: {
      borderDash: [2],
      borderDashOffset: [2],
      color: "dark" == settings.charts.colorScheme ? settings.colors.gray[900] : settings.colors.gray[100],
      drawBorder: !1,
      drawTicks: !1,
      lineWidth: 0,
      zeroLineWidth: 0,
      zeroLineColor: "dark" == settings.charts.colorScheme ? settings.colors.gray[900] : settings.colors.gray[100],
      zeroLineBorderDash: [2],
      zeroLineBorderDashOffset: [2]
    },
    ticks: {
      beginAtZero: !0,
      padding: 10,
      callback: function callback(a) {
        if (!(a % 10)) return a;
      }
    }
  });
  Chart.scaleService.updateScaleDefaults("category", {
    gridLines: {
      drawBorder: !1,
      drawOnChartArea: !1,
      drawTicks: !1
    },
    ticks: {
      padding: 20
    },
    maxBarThickness: 10
  });
  $('[data-toggle="chart"]').on({
    change: function change() {
      var el = $(this);

      if (el.is("[data-add]")) {
        add(el);
      }
    },
    click: function click() {
      var el = $(this);

      if (el.is("[data-update]")) {
        update(el);
      }
    }
  });
};

var Charts = {
  settings: settings,
  init: init,
  add: add,
  update: update,
  create: create
};

if (window !== undefined) {
  window.Charts = Charts;
}

/***/ }),

/***/ 14:
/*!****************************************!*\
  !*** multi ./src/js/plugins/charts.js ***!
  \****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /Users/demi/Documents/GitHub/admin-educate/src/js/plugins/charts.js */"./src/js/plugins/charts.js");


/***/ })

/******/ });
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vd2VicGFjay9ib290c3RyYXAiLCJ3ZWJwYWNrOi8vLy4vbm9kZV9tb2R1bGVzL0BiYWJlbC9ydW50aW1lL2hlbHBlcnMvdHlwZW9mLmpzIiwid2VicGFjazovLy8uL3NyYy9qcy9wbHVnaW5zL2NoYXJ0cy5qcyJdLCJuYW1lcyI6WyJleHRlbmQiLCJ2YWx1ZSIsIm9iamVjdCIsImFkZCIsImRhdGEiLCJlbGVtZW50IiwiY2hhcnQiLCIkIiwiYWRkUmVjdXJzaXZlIiwiQXJyYXkiLCJyZW1vdmVSZWN1cnNpdmUiLCJ1cGRhdGUiLCJwcmVmaXgiLCJzdWZmaXgiLCJhIiwidCIsImUiLCJvIiwiciIsImdsb2JhbFNldHRpbmdzIiwicmVzcG9uc2l2ZSIsIm1haW50YWluQXNwZWN0UmF0aW8iLCJkZWZhdWx0Q29sb3IiLCJzZXR0aW5ncyIsImRlZmF1bHRGb250Q29sb3IiLCJkZWZhdWx0Rm9udEZhbWlseSIsImRlZmF1bHRGb250U2l6ZSIsImxheW91dCIsInBhZGRpbmciLCJsZWdlbmQiLCJkaXNwbGF5IiwicG9zaXRpb24iLCJsYWJlbHMiLCJ1c2VQb2ludFN0eWxlIiwiZWxlbWVudHMiLCJwb2ludCIsInJhZGl1cyIsImJhY2tncm91bmRDb2xvciIsImxpbmUiLCJ0ZW5zaW9uIiwiYm9yZGVyV2lkdGgiLCJib3JkZXJDb2xvciIsImJvcmRlckNhcFN0eWxlIiwicmVjdGFuZ2xlIiwiYXJjIiwidG9vbHRpcHMiLCJlbmFibGVkIiwibW9kZSIsImludGVyc2VjdCIsImN1c3RvbSIsImwiLCJuIiwicyIsImkiLCJjIiwiZCIsInUiLCJ0b3AiLCJsZWZ0IiwiY2FsbGJhY2tzIiwibGFiZWwiLCJkb3VnaG51dFNldHRpbmdzIiwiY3V0b3V0UGVyY2VudGFnZSIsInRpdGxlIiwibGVnZW5kQ2FsbGJhY2siLCJjcmVhdGUiLCJ0eXBlIiwib3B0aW9ucyIsImRvY3VtZW50IiwiaW5pdCIsImRlZmF1bHRzIiwiZ2xvYmFsIiwiZG91Z2hudXQiLCJDaGFydCIsImdyaWRMaW5lcyIsImJvcmRlckRhc2giLCJib3JkZXJEYXNoT2Zmc2V0IiwiY29sb3IiLCJkcmF3Qm9yZGVyIiwiZHJhd1RpY2tzIiwibGluZVdpZHRoIiwiemVyb0xpbmVXaWR0aCIsInplcm9MaW5lQ29sb3IiLCJ6ZXJvTGluZUJvcmRlckRhc2giLCJ6ZXJvTGluZUJvcmRlckRhc2hPZmZzZXQiLCJ0aWNrcyIsImJlZ2luQXRaZXJvIiwiY2FsbGJhY2siLCJkcmF3T25DaGFydEFyZWEiLCJtYXhCYXJUaGlja25lc3MiLCJjaGFuZ2UiLCJlbCIsImNsaWNrIiwiQ2hhcnRzIiwid2luZG93Il0sIm1hcHBpbmdzIjoiO1FBQUE7UUFDQTs7UUFFQTtRQUNBOztRQUVBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBOztRQUVBO1FBQ0E7O1FBRUE7UUFDQTs7UUFFQTtRQUNBO1FBQ0E7OztRQUdBO1FBQ0E7O1FBRUE7UUFDQTs7UUFFQTtRQUNBO1FBQ0E7UUFDQSwwQ0FBMEMsZ0NBQWdDO1FBQzFFO1FBQ0E7O1FBRUE7UUFDQTtRQUNBO1FBQ0Esd0RBQXdELGtCQUFrQjtRQUMxRTtRQUNBLGlEQUFpRCxjQUFjO1FBQy9EOztRQUVBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQSx5Q0FBeUMsaUNBQWlDO1FBQzFFLGdIQUFnSCxtQkFBbUIsRUFBRTtRQUNySTtRQUNBOztRQUVBO1FBQ0E7UUFDQTtRQUNBLDJCQUEyQiwwQkFBMEIsRUFBRTtRQUN2RCxpQ0FBaUMsZUFBZTtRQUNoRDtRQUNBO1FBQ0E7O1FBRUE7UUFDQSxzREFBc0QsK0RBQStEOztRQUVySDtRQUNBOzs7UUFHQTtRQUNBOzs7Ozs7Ozs7Ozs7QUNsRkE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEdBQUc7QUFDSDtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBLHlCOzs7Ozs7Ozs7Ozs7O0FDaEJBLElBQU1BLE1BQU0sR0FB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QyxhQUFTLEVBQUU7QUFDVEksZ0JBQVUsRUFBRSxDQURIO0FBRVRVLHFCQUFlLEVBQUUsQ0FGUjtBQUdUVCxlQUFTLEVBQUUsQ0FBQztBQUhILEtBRHNDO0FBTWpETSxTQUFLLEVBQUU7QUFDTHpELGFBQU8sRUFBRTtBQURKLEtBTjBDO0FBU2pENkQsbUJBQWUsRUFBRTtBQVRnQyxHQUFuRGhCO0FBWUFsRSxHQUFDLENBQURBLHVCQUFDLENBQURBLElBQThCO0FBQzVCbUYsVUFBTSxFQUFFLGtCQUFXO0FBQ2pCLFVBQUlDLEVBQUUsR0FBR3BGLENBQUMsQ0FBVixJQUFVLENBQVY7O0FBQ0EsVUFBSW9GLEVBQUUsQ0FBRkEsR0FBSixZQUFJQSxDQUFKLEVBQXlCO0FBQ3ZCeEYsV0FBRyxDQUFIQSxFQUFHLENBQUhBO0FBQ0Q7QUFMeUI7QUFPNUJ5RixTQUFLLEVBQUUsaUJBQVc7QUFDaEIsVUFBSUQsRUFBRSxHQUFHcEYsQ0FBQyxDQUFWLElBQVUsQ0FBVjs7QUFDQSxVQUFJb0YsRUFBRSxDQUFGQSxHQUFKLGVBQUlBLENBQUosRUFBNEI7QUFDMUJoRixjQUFNLENBQU5BLEVBQU0sQ0FBTkE7QUFDRDtBQUNGO0FBWjJCLEdBQTlCSjtBQTFDRjs7QUEwREEsSUFBTXNGLE1BQU0sR0FBRztBQUNidEUsVUFBUSxFQURLO0FBRWI4QyxNQUFJLEVBRlM7QUFHYmxFLEtBQUcsRUFIVTtBQUliUSxRQUFNLEVBSk87QUFLYnNELFFBQU0sRUFBTkE7QUFMYSxDQUFmOztBQVFBLElBQUk2QixNQUFNLEtBQVYsV0FBMEI7QUFDeEJBLFFBQU0sQ0FBTkE7QUFDRCxDIiwiZmlsZSI6Ii9kaXN0L2Fzc2V0cy9qcy9jaGFydHMuanMiLCJzb3VyY2VzQ29udGVudCI6WyIgXHQvLyBUaGUgbW9kdWxlIGNhY2hlXG4gXHR2YXIgaW5zdGFsbGVkTW9kdWxlcyA9IHt9O1xuXG4gXHQvLyBUaGUgcmVxdWlyZSBmdW5jdGlvblxuIFx0ZnVuY3Rpb24gX193ZWJwYWNrX3JlcXVpcmVfXyhtb2R1bGVJZCkge1xuXG4gXHRcdC8vIENoZWNrIGlmIG1vZHVsZSBpcyBpbiBjYWNoZVxuIFx0XHRpZihpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXSkge1xuIFx0XHRcdHJldHVybiBpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXS5leHBvcnRzO1xuIFx0XHR9XG4gXHRcdC8vIENyZWF0ZSBhIG5ldyBtb2R1bGUgKGFuZCBwdXQgaXQgaW50byB0aGUgY2FjaGUpXG4gXHRcdHZhciBtb2R1bGUgPSBpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXSA9IHtcbiBcdFx0XHRpOiBtb2R1bGVJZCxcbiBcdFx0XHRsOiBmYWxzZSxcbiBcdFx0XHRleHBvcnRzOiB7fVxuIFx0XHR9O1xuXG4gXHRcdC8vIEV4ZWN1dGUgdGhlIG1vZHVsZSBmdW5jdGlvblxuIFx0XHRtb2R1bGVzW21vZHVsZUlkXS5jYWxsKG1vZHVsZS5leHBvcnRzLCBtb2R1bGUsIG1vZHVsZS5leHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKTtcblxuIFx0XHQvLyBGbGFnIHRoZSBtb2R1bGUgYXMgbG9hZGVkXG4gXHRcdG1vZHVsZS5sID0gdHJ1ZTtcblxuIFx0XHQvLyBSZXR1cm4gdGhlIGV4cG9ydHMgb2YgdGhlIG1vZHVsZVxuIFx0XHRyZXR1cm4gbW9kdWxlLmV4cG9ydHM7XG4gXHR9XG5cblxuIFx0Ly8gZXhwb3NlIHRoZSBtb2R1bGVzIG9iamVjdCAoX193ZWJwYWNrX21vZHVsZXNfXylcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubSA9IG1vZHVsZXM7XG5cbiBcdC8vIGV4cG9zZSB0aGUgbW9kdWxlIGNhY2hlXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLmMgPSBpbnN0YWxsZWRNb2R1bGVzO1xuXG4gXHQvLyBkZWZpbmUgZ2V0dGVyIGZ1bmN0aW9uIGZvciBoYXJtb255IGV4cG9ydHNcbiBcdF9fd2VicGFja19yZXF1aXJlX18uZCA9IGZ1bmN0aW9uKGV4cG9ydHMsIG5hbWUsIGdldHRlcikge1xuIFx0XHRpZighX193ZWJwYWNrX3JlcXVpcmVfXy5vKGV4cG9ydHMsIG5hbWUpKSB7XG4gXHRcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIG5hbWUsIHsgZW51bWVyYWJsZTogdHJ1ZSwgZ2V0OiBnZXR0ZXIgfSk7XG4gXHRcdH1cbiBcdH07XG5cbiBcdC8vIGRlZmluZSBfX2VzTW9kdWxlIG9uIGV4cG9ydHNcbiBcdF9fd2VicGFja19yZXF1aXJlX18uciA9IGZ1bmN0aW9uKGV4cG9ydHMpIHtcbiBcdFx0aWYodHlwZW9mIFN5bWJvbCAhPT0gJ3VuZGVmaW5lZCcgJiYgU3ltYm9sLnRvU3RyaW5nVGFnKSB7XG4gXHRcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFN5bWJvbC50b1N0cmluZ1RhZywgeyB2YWx1ZTogJ01vZHVsZScgfSk7XG4gXHRcdH1cbiBcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsICdfX2VzTW9kdWxlJywgeyB2YWx1ZTogdHJ1ZSB9KTtcbiBcdH07XG5cbiBcdC8vIGNyZWF0ZSBhIGZha2UgbmFtZXNwYWNlIG9iamVjdFxuIFx0Ly8gbW9kZSAmIDE6IHZhbHVlIGlzIGEgbW9kdWxlIGlkLCByZXF1aXJlIGl0XG4gXHQvLyBtb2RlICYgMjogbWVyZ2UgYWxsIHByb3BlcnRpZXMgb2YgdmFsdWUgaW50byB0aGUgbnNcbiBcdC8vIG1vZGUgJiA0OiByZXR1cm4gdmFsdWUgd2hlbiBhbHJlYWR5IG5zIG9iamVjdFxuIFx0Ly8gbW9kZSAmIDh8MTogYmVoYXZlIGxpa2UgcmVxdWlyZVxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy50ID0gZnVuY3Rpb24odmFsdWUsIG1vZGUpIHtcbiBcdFx0aWYobW9kZSAmIDEpIHZhbHVlID0gX193ZWJwYWNrX3JlcXVpcmVfXyh2YWx1ZSk7XG4gXHRcdGlmKG1vZGUgJiA4KSByZXR1cm4gdmFsdWU7XG4gXHRcdGlmKChtb2RlICYgNCkgJiYgdHlwZW9mIHZhbHVlID09PSAnb2JqZWN0JyAmJiB2YWx1ZSAmJiB2YWx1ZS5fX2VzTW9kdWxlKSByZXR1cm4gdmFsdWU7XG4gXHRcdHZhciBucyA9IE9iamVjdC5jcmVhdGUobnVsbCk7XG4gXHRcdF9fd2VicGFja19yZXF1aXJlX18ucihucyk7XG4gXHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShucywgJ2RlZmF1bHQnLCB7IGVudW1lcmFibGU6IHRydWUsIHZhbHVlOiB2YWx1ZSB9KTtcbiBcdFx0aWYobW9kZSAmIDIgJiYgdHlwZW9mIHZhbHVlICE9ICdzdHJpbmcnKSBmb3IodmFyIGtleSBpbiB2YWx1ZSkgX193ZWJwYWNrX3JlcXVpcmVfXy5kKG5zLCBrZXksIGZ1bmN0aW9uKGtleSkgeyByZXR1cm4gdmFsdWVba2V5XTsgfS5iaW5kKG51bGwsIGtleSkpO1xuIFx0XHRyZXR1cm4gbnM7XG4gXHR9O1xuXG4gXHQvLyBnZXREZWZhdWx0RXhwb3J0IGZ1bmN0aW9uIGZvciBjb21wYXRpYmlsaXR5IHdpdGggbm9uLWhhcm1vbnkgbW9kdWxlc1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5uID0gZnVuY3Rpb24obW9kdWxlKSB7XG4gXHRcdHZhciBnZXR0ZXIgPSBtb2R1bGUgJiYgbW9kdWxlLl9fZXNNb2R1bGUgP1xuIFx0XHRcdGZ1bmN0aW9uIGdldERlZmF1bHQoKSB7IHJldHVybiBtb2R1bGVbJ2RlZmF1bHQnXTsgfSA6XG4gXHRcdFx0ZnVuY3Rpb24gZ2V0TW9kdWxlRXhwb3J0cygpIHsgcmV0dXJuIG1vZHVsZTsgfTtcbiBcdFx0X193ZWJwYWNrX3JlcXVpcmVfXy5kKGdldHRlciwgJ2EnLCBnZXR0ZXIpO1xuIFx0XHRyZXR1cm4gZ2V0dGVyO1xuIFx0fTtcblxuIFx0Ly8gT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLm8gPSBmdW5jdGlvbihvYmplY3QsIHByb3BlcnR5KSB7IHJldHVybiBPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwob2JqZWN0LCBwcm9wZXJ0eSk7IH07XG5cbiBcdC8vIF9fd2VicGFja19wdWJsaWNfcGF0aF9fXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLnAgPSBcIi9cIjtcblxuXG4gXHQvLyBMb2FkIGVudHJ5IG1vZHVsZSBhbmQgcmV0dXJuIGV4cG9ydHNcbiBcdHJldHVybiBfX3dlYnBhY2tfcmVxdWlyZV9fKF9fd2VicGFja19yZXF1aXJlX18ucyA9IDE0KTtcbiIsImZ1bmN0aW9uIF90eXBlb2Yob2JqKSB7XG4gIFwiQGJhYmVsL2hlbHBlcnMgLSB0eXBlb2ZcIjtcblxuICBpZiAodHlwZW9mIFN5bWJvbCA9PT0gXCJmdW5jdGlvblwiICYmIHR5cGVvZiBTeW1ib2wuaXRlcmF0b3IgPT09IFwic3ltYm9sXCIpIHtcbiAgICBtb2R1bGUuZXhwb3J0cyA9IF90eXBlb2YgPSBmdW5jdGlvbiBfdHlwZW9mKG9iaikge1xuICAgICAgcmV0dXJuIHR5cGVvZiBvYmo7XG4gICAgfTtcbiAgfSBlbHNlIHtcbiAgICBtb2R1bGUuZXhwb3J0cyA9IF90eXBlb2YgPSBmdW5jdGlvbiBfdHlwZW9mKG9iaikge1xuICAgICAgcmV0dXJuIG9iaiAmJiB0eXBlb2YgU3ltYm9sID09PSBcImZ1bmN0aW9uXCIgJiYgb2JqLmNvbnN0cnVjdG9yID09PSBTeW1ib2wgJiYgb2JqICE9PSBTeW1ib2wucHJvdG90eXBlID8gXCJzeW1ib2xcIiA6IHR5cGVvZiBvYmo7XG4gICAgfTtcbiAgfVxuXG4gIHJldHVybiBfdHlwZW9mKG9iaik7XG59XG5cbm1vZHVsZS5leHBvcnRzID0gX3R5cGVvZjsiLCJjb25zdCBleHRlbmQgPSAob2JqZWN0LCB2YWx1ZSkgPT4ge1xuICBmb3IgKHZhciBrZXkgaW4gdmFsdWUpIFwib2JqZWN0XCIgIT0gdHlwZW9mIHZhbHVlW2tleV0gPyBvYmplY3Rba2V5XSA9IHZhbHVlW2tleV0gOiBleHRlbmQob2JqZWN0W2tleV0sIHZhbHVlW2tleV0pXG59XG5cbmNvbnN0IGFkZCA9IChlbGVtZW50KSA9PiB7XG4gIHZhciBkYXRhID0gZWxlbWVudC5kYXRhKFwiYWRkXCIpXG4gIHZhciBjaGFydCA9ICQoZWxlbWVudC5kYXRhKFwidGFyZ2V0XCIpKS5kYXRhKFwiY2hhcnRcIilcblxuICBpZiAoZWxlbWVudC5pcyhcIjpjaGVja2VkXCIpKSB7XG4gICAgZnVuY3Rpb24gYWRkUmVjdXJzaXZlKGNoYXJ0LCBkYXRhKSB7XG4gICAgICBmb3IgKHZhciBvIGluIGRhdGEpIEFycmF5LmlzQXJyYXkoZGF0YVtvXSkgPyBkYXRhW29dLmZvckVhY2goZnVuY3Rpb24oYSkge1xuICAgICAgICBjaGFydFtvXS5wdXNoKGEpXG4gICAgICB9KSA6IGFkZFJlY3Vyc2l2ZShjaGFydFtvXSwgZGF0YVtvXSlcbiAgICB9XG4gICAgYWRkUmVjdXJzaXZlKGNoYXJ0LCBkYXRhKVxuICB9IFxuICBlbHNlIHtcbiAgICBmdW5jdGlvbiByZW1vdmVSZWN1cnNpdmUoY2hhcnQsIGRhdGEpIHtcbiAgICAgIGZvciAodmFyIG8gaW4gZGF0YSkgQXJyYXkuaXNBcnJheShkYXRhW29dKSA/IGRhdGFbb10uZm9yRWFjaChmdW5jdGlvbihhKSB7XG4gICAgICAgIGNoYXJ0W29dLnBvcCgpXG4gICAgICB9KSA6IHJlbW92ZVJlY3Vyc2l2ZShjaGFydFtvXSwgZGF0YVtvXSlcbiAgICB9XG4gICAgcmVtb3ZlUmVjdXJzaXZlKGNoYXJ0LCBkYXRhKVxuICB9XG5cbiAgY2hhcnQudXBkYXRlKClcbn1cblxuY29uc3QgdXBkYXRlID0gKGVsZW1lbnQpID0+IHtcbiAgdmFyIGRhdGEgPSBlbGVtZW50LmRhdGEoXCJ1cGRhdGVcIilcbiAgdmFyIGNoYXJ0ID0gJChlbGVtZW50LmRhdGEoXCJ0YXJnZXRcIikpLmRhdGEoXCJjaGFydFwiKVxuICBcbiAgZXh0ZW5kKGNoYXJ0LCBkYXRhKVxuXG4gIGlmICh2b2lkIDAgIT09IGVsZW1lbnQuZGF0YShcInByZWZpeFwiKSB8fCB2b2lkIDAgIT09IGVsZW1lbnQuZGF0YShcInN1ZmZpeFwiKSkge1xuICAgIGxldCBwcmVmaXggPSBlbGVtZW50LmRhdGEoXCJwcmVmaXhcIikgPyBlbGVtZW50LmRhdGEoXCJwcmVmaXhcIikgOiBcIlwiXG4gICAgbGV0IHN1ZmZpeCA9IGVsZW1lbnQuZGF0YShcInN1ZmZpeFwiKSA/IGVsZW1lbnQuZGF0YShcInN1ZmZpeFwiKSA6IFwiXCJcblxuICAgIGlmIChjaGFydC5vcHRpb25zLnNjYWxlcyAhPT0gdW5kZWZpbmVkKSB7XG4gICAgICBjaGFydC5vcHRpb25zLnNjYWxlcy55QXhlc1swXS50aWNrcy5jYWxsYmFjayA9IGZ1bmN0aW9uKGEpIHtcbiAgICAgICAgaWYgKCEoYSAlIDEwKSkgcmV0dXJuIHByZWZpeCArIGEgKyBzdWZmaXhcbiAgICAgIH1cbiAgICB9XG5cbiAgICBjaGFydC5vcHRpb25zLnRvb2x0aXBzLmNhbGxiYWNrcy5sYWJlbCA9IGZ1bmN0aW9uKGEsIGUpIHtcbiAgICAgIHZhciB0ID0gZS5kYXRhc2V0c1thLmRhdGFzZXRJbmRleF0ubGFiZWwgfHwgXCJcIixcbiAgICAgICAgICBvID0gYS55TGFiZWwgfHwgZS5kYXRhc2V0c1swXS5kYXRhW2EuaW5kZXhdLFxuICAgICAgICAgIHIgPSBcIlwiO1xuICAgICAgcmV0dXJuIDEgPCBlLmRhdGFzZXRzLmxlbmd0aCAmJiAociArPSAnPHNwYW4gY2xhc3M9XCJwb3BvdmVyLWJvZHktbGFiZWwgbXItYXV0b1wiPicgKyB0ICsgXCI8L3NwYW4+XCIpLCByICs9ICc8c3BhbiBjbGFzcz1cInBvcG92ZXItYm9keS12YWx1ZVwiPicgKyBwcmVmaXggKyBvICsgc3VmZml4ICsgXCI8L3NwYW4+XCJcbiAgICB9XG4gIH1cblxuICBjaGFydC51cGRhdGUoKVxufVxuXG5jb25zdCBnbG9iYWxTZXR0aW5ncyA9IHtcbiAgcmVzcG9uc2l2ZTogdHJ1ZSxcbiAgbWFpbnRhaW5Bc3BlY3RSYXRpbzogZmFsc2UsXG4gIGRlZmF1bHRDb2xvcjogXCJkYXJrXCIgPT0gc2V0dGluZ3MuY2hhcnRzLmNvbG9yU2NoZW1lID8gc2V0dGluZ3MuY29sb3JzLmdyYXlbNzAwXSA6IHNldHRpbmdzLmNvbG9ycy5ncmF5WzYwMF0sXG4gIGRlZmF1bHRGb250Q29sb3I6IFwiZGFya1wiID09IHNldHRpbmdzLmNoYXJ0cy5jb2xvclNjaGVtZSA/IHNldHRpbmdzLmNvbG9ycy5ncmF5WzcwMF0gOiBzZXR0aW5ncy5jb2xvcnMuZ3JheVs2MDBdLFxuICBkZWZhdWx0Rm9udEZhbWlseTogc2V0dGluZ3MuZm9udHMuYmFzZSxcbiAgZGVmYXVsdEZvbnRTaXplOiAxMyxcbiAgbGF5b3V0OiB7XG4gICAgcGFkZGluZzogMFxuICB9LFxuICBsZWdlbmQ6IHtcbiAgICBkaXNwbGF5OiBmYWxzZSxcbiAgICBwb3NpdGlvbjogXCJib3R0b21cIixcbiAgICBsYWJlbHM6IHtcbiAgICAgIHVzZVBvaW50U3R5bGU6IHRydWUsXG4gICAgICBwYWRkaW5nOiAxNlxuICAgIH1cbiAgfSxcbiAgZWxlbWVudHM6IHtcbiAgICBwb2ludDoge1xuICAgICAgcmFkaXVzOiAwLFxuICAgICAgYmFja2dyb3VuZENvbG9yOiBzZXR0aW5ncy5jb2xvcnMucHJpbWFyeVs1MDBdXG4gICAgfSxcbiAgICBsaW5lOiB7XG4gICAgICB0ZW5zaW9uOiAuNCxcbiAgICAgIGJvcmRlcldpZHRoOiAzLFxuICAgICAgYm9yZGVyQ29sb3I6IHNldHRpbmdzLmNvbG9ycy5wcmltYXJ5WzUwMF0sXG4gICAgICBiYWNrZ3JvdW5kQ29sb3I6IHNldHRpbmdzLmNvbG9ycy50cmFuc3BhcmVudCxcbiAgICAgIGJvcmRlckNhcFN0eWxlOiBcInJvdW5kZWRcIlxuICAgIH0sXG4gICAgcmVjdGFuZ2xlOiB7XG4gICAgICBiYWNrZ3JvdW5kQ29sb3I6IHNldHRpbmdzLmNvbG9ycy5wcmltYXJ5WzUwMF1cbiAgICB9LFxuICAgIGFyYzoge1xuICAgICAgYmFja2dyb3VuZENvbG9yOiBzZXR0aW5ncy5jb2xvcnMucHJpbWFyeVs1MDBdLFxuICAgICAgYm9yZGVyQ29sb3I6IFwiZGFya1wiID09IHNldHRpbmdzLmNoYXJ0cy5jb2xvclNjaGVtZSA/IHNldHRpbmdzLmNvbG9ycy5ncmF5WzgwMF0gOiBzZXR0aW5ncy5jb2xvcnMud2hpdGUsXG4gICAgICBib3JkZXJXaWR0aDogNFxuICAgIH1cbiAgfSxcbiAgdG9vbHRpcHM6IHtcbiAgICBlbmFibGVkOiAhMSxcbiAgICBtb2RlOiBcImluZGV4XCIsXG4gICAgaW50ZXJzZWN0OiAhMSxcbiAgICBjdXN0b206IGZ1bmN0aW9uKHIpIHtcbiAgICAgIHZhciBhID0gJChcIiNjaGFydC10b29sdGlwXCIpO1xuICAgICAgaWYgKGEubGVuZ3RoIHx8IChhID0gJCgnPGRpdiBpZD1cImNoYXJ0LXRvb2x0aXBcIiBjbGFzcz1cInBvcG92ZXIgYnMtcG9wb3Zlci10b3BcIiByb2xlPVwidG9vbHRpcFwiPjwvZGl2PicpLCAkKFwiYm9keVwiKS5hcHBlbmQoYSkpLCAwICE9PSByLm9wYWNpdHkpIHtcbiAgICAgICAgaWYgKHIuYm9keSkge1xuICAgICAgICAgIHZhciBlID0gci50aXRsZSB8fCBbXSxcbiAgICAgICAgICAgICAgbCA9IHIuYm9keS5tYXAoZnVuY3Rpb24oYSkge1xuICAgICAgICAgICAgICAgIHJldHVybiBhLmxpbmVzXG4gICAgICAgICAgICAgIH0pLFxuICAgICAgICAgICAgICBuID0gXCJcIjtcbiAgICAgICAgICBuICs9ICc8ZGl2IGNsYXNzPVwiYXJyb3dcIj48L2Rpdj4nLCBlLmZvckVhY2goZnVuY3Rpb24oYSkge1xuICAgICAgICAgICAgICBuICs9ICc8aDMgY2xhc3M9XCJwb3BvdmVyLWhlYWRlciB0ZXh0LWNlbnRlclwiPicgKyBhICsgXCI8L2gzPlwiXG4gICAgICAgICAgfSksIGwuZm9yRWFjaChmdW5jdGlvbihhLCBlKSB7XG4gICAgICAgICAgICAgIHZhciB0ID0gJzxzcGFuIGNsYXNzPVwicG9wb3Zlci1ib2R5LWluZGljYXRvclwiIHN0eWxlPVwiYmFja2dyb3VuZC1jb2xvcjogJyArIHIubGFiZWxDb2xvcnNbZV0uYmFja2dyb3VuZENvbG9yICsgJ1wiPjwvc3Bhbj4nLFxuICAgICAgICAgICAgICAgICAgbyA9IDEgPCBsLmxlbmd0aCA/IFwianVzdGlmeS1jb250ZW50LWxlZnRcIiA6IFwianVzdGlmeS1jb250ZW50LWNlbnRlclwiO1xuICAgICAgICAgICAgICBuICs9ICc8ZGl2IGNsYXNzPVwicG9wb3Zlci1ib2R5IGQtZmxleCBhbGlnbi1pdGVtcy1jZW50ZXIgJyArIG8gKyAnXCI+JyArIHQgKyBhICsgXCI8L2Rpdj5cIlxuICAgICAgICAgIH0pLCBhLmh0bWwobilcbiAgICAgICAgfVxuICAgICAgICB2YXIgdCA9ICQodGhpcy5fY2hhcnQuY2FudmFzKSxcbiAgICAgICAgICAgIG8gPSAodC5vdXRlcldpZHRoKCksIHQub3V0ZXJIZWlnaHQoKSwgdC5vZmZzZXQoKS50b3ApLFxuICAgICAgICAgICAgcyA9IHQub2Zmc2V0KCkubGVmdCxcbiAgICAgICAgICAgIGkgPSBhLm91dGVyV2lkdGgoKSxcbiAgICAgICAgICAgIGMgPSBhLm91dGVySGVpZ2h0KCksXG4gICAgICAgICAgICBkID0gbyArIHIuY2FyZXRZIC0gYyAtIDE2LFxuICAgICAgICAgICAgdSA9IHMgKyByLmNhcmV0WCAtIGkgLyAyO1xuICAgICAgICAgIFxuICAgICAgICBhLmNzcyh7XG4gICAgICAgICAgdG9wOiBkICsgXCJweFwiLFxuICAgICAgICAgIGxlZnQ6IHUgKyBcInB4XCIsXG4gICAgICAgICAgZGlzcGxheTogXCJibG9ja1wiXG4gICAgICAgIH0pXG5cbiAgICAgIH0gZWxzZSBhLmNzcyhcImRpc3BsYXlcIiwgXCJub25lXCIpXG4gICAgfSxcbiAgICBjYWxsYmFja3M6IHtcbiAgICAgIGxhYmVsOiBmdW5jdGlvbihhLCBlKSB7XG4gICAgICAgIHZhciB0ID0gZS5kYXRhc2V0c1thLmRhdGFzZXRJbmRleF0ubGFiZWwgfHwgXCJcIixcbiAgICAgICAgICAgIG8gPSBhLnlMYWJlbCxcbiAgICAgICAgICAgIHIgPSBcIlwiO1xuICAgICAgICByZXR1cm4gMSA8IGUuZGF0YXNldHMubGVuZ3RoICYmIChyICs9ICc8c3BhbiBjbGFzcz1cInBvcG92ZXItYm9keS1sYWJlbCBtci1hdXRvXCI+JyArIHQgKyBcIjwvc3Bhbj5cIiksIHIgKz0gJzxzcGFuIGNsYXNzPVwicG9wb3Zlci1ib2R5LXZhbHVlXCI+JyArIG8gKyBcIjwvc3Bhbj5cIlxuICAgICAgfVxuICAgIH1cbiAgfVxufVxuXG5jb25zdCBkb3VnaG51dFNldHRpbmdzID0ge1xuICBjdXRvdXRQZXJjZW50YWdlOiA4MyxcbiAgdG9vbHRpcHM6IHtcbiAgICBjYWxsYmFja3M6IHtcbiAgICAgIHRpdGxlOiBmdW5jdGlvbihhLCBlKSB7XG4gICAgICAgIHJldHVybiBlLmxhYmVsc1thWzBdLmluZGV4XVxuICAgICAgfSxcbiAgICAgIGxhYmVsOiBmdW5jdGlvbihhLCBlKSB7XG4gICAgICAgIHZhciB0ID0gXCJcIjtcbiAgICAgICAgcmV0dXJuIHQgKz0gJzxzcGFuIGNsYXNzPVwicG9wb3Zlci1ib2R5LXZhbHVlXCI+JyArIGUuZGF0YXNldHNbMF0uZGF0YVthLmluZGV4XSArIFwiPC9zcGFuPlwiXG4gICAgICB9XG4gICAgfVxuICB9LFxuICBsZWdlbmRDYWxsYmFjazogZnVuY3Rpb24oYSkge1xuICAgIHZhciBvID0gYS5kYXRhLFxuICAgICAgICByID0gXCJcIjtcbiAgICByZXR1cm4gby5sYWJlbHMuZm9yRWFjaChmdW5jdGlvbihhLCBlKSB7XG4gICAgICB2YXIgdCA9IG8uZGF0YXNldHNbMF0uYmFja2dyb3VuZENvbG9yW2VdO1xuICAgICAgciArPSAnPHNwYW4gY2xhc3M9XCJjaGFydC1sZWdlbmQtaXRlbVwiPicsIHIgKz0gJzxpIGNsYXNzPVwiY2hhcnQtbGVnZW5kLWluZGljYXRvclwiIHN0eWxlPVwiYmFja2dyb3VuZC1jb2xvcjogJyArIHQgKyAnXCI+PC9pPicsIHIgKz0gYSwgciArPSBcIjwvc3Bhbj5cIlxuICAgIH0pLCByXG4gIH1cbn1cblxuY29uc3QgY3JlYXRlID0gKGlkLCB0eXBlID0gJ2xpbmUnLCBvcHRpb25zID0ge30sIGRhdGEgPSB7fSkgPT4ge1xuICB2YXIgZWxlbWVudCA9ICQoaWQpXG4gIHZhciBjaGFydCA9IG5ldyBDaGFydChlbGVtZW50LCB7XG4gICAgdHlwZTogdHlwZSxcbiAgICBvcHRpb25zOiBvcHRpb25zLFxuICAgIGRhdGE6IGRhdGFcbiAgfSlcbiAgZWxlbWVudC5kYXRhKFwiY2hhcnRcIiwgY2hhcnQpXG4gIGlmIChlbGVtZW50LmRhdGEoXCJjaGFydC1sZWdlbmRcIikpIHtcbiAgICBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKGVsZW1lbnQuZGF0YShcImNoYXJ0LWxlZ2VuZFwiKSlcbiAgICAgIC5pbm5lckhUTUwgPSBjaGFydC5nZW5lcmF0ZUxlZ2VuZCgpXG4gIH1cbn1cblxuY29uc3QgaW5pdCA9ICgpID0+IHtcbiAgZXh0ZW5kKENoYXJ0LCB7XG4gICAgZGVmYXVsdHM6IHtcbiAgICAgIGdsb2JhbDogZ2xvYmFsU2V0dGluZ3MsXG4gICAgICBkb3VnaG51dDogZG91Z2hudXRTZXR0aW5nc1xuICAgIH1cbiAgfSlcblxuICBDaGFydC5zY2FsZVNlcnZpY2UudXBkYXRlU2NhbGVEZWZhdWx0cyhcImxpbmVhclwiLCB7XG4gICAgZ3JpZExpbmVzOiB7XG4gICAgICBib3JkZXJEYXNoOiBbMl0sXG4gICAgICBib3JkZXJEYXNoT2Zmc2V0OiBbMl0sXG4gICAgICBjb2xvcjogXCJkYXJrXCIgPT0gc2V0dGluZ3MuY2hhcnRzLmNvbG9yU2NoZW1lID8gc2V0dGluZ3MuY29sb3JzLmdyYXlbOTAwXSA6IHNldHRpbmdzLmNvbG9ycy5ncmF5WzEwMF0sXG4gICAgICBkcmF3Qm9yZGVyOiAhMSxcbiAgICAgIGRyYXdUaWNrczogITEsXG4gICAgICBsaW5lV2lkdGg6IDAsXG4gICAgICB6ZXJvTGluZVdpZHRoOiAwLFxuICAgICAgemVyb0xpbmVDb2xvcjogXCJkYXJrXCIgPT0gc2V0dGluZ3MuY2hhcnRzLmNvbG9yU2NoZW1lID8gc2V0dGluZ3MuY29sb3JzLmdyYXlbOTAwXSA6IHNldHRpbmdzLmNvbG9ycy5ncmF5WzEwMF0sXG4gICAgICB6ZXJvTGluZUJvcmRlckRhc2g6IFsyXSxcbiAgICAgIHplcm9MaW5lQm9yZGVyRGFzaE9mZnNldDogWzJdXG4gICAgfSxcbiAgICB0aWNrczoge1xuICAgICAgYmVnaW5BdFplcm86ICEwLFxuICAgICAgcGFkZGluZzogMTAsXG4gICAgICBjYWxsYmFjazogZnVuY3Rpb24oYSkge1xuICAgICAgICBpZiAoIShhICUgMTApKSByZXR1cm4gYVxuICAgICAgfVxuICAgIH1cbiAgfSlcblxuICBDaGFydC5zY2FsZVNlcnZpY2UudXBkYXRlU2NhbGVEZWZhdWx0cyhcImNhdGVnb3J5XCIsIHtcbiAgICBncmlkTGluZXM6IHtcbiAgICAgIGRyYXdCb3JkZXI6ICExLFxuICAgICAgZHJhd09uQ2hhcnRBcmVhOiAhMSxcbiAgICAgIGRyYXdUaWNrczogITFcbiAgICB9LFxuICAgIHRpY2tzOiB7XG4gICAgICBwYWRkaW5nOiAyMFxuICAgIH0sXG4gICAgbWF4QmFyVGhpY2tuZXNzOiAxMFxuICB9KVxuXG4gICQoJ1tkYXRhLXRvZ2dsZT1cImNoYXJ0XCJdJykub24oe1xuICAgIGNoYW5nZTogZnVuY3Rpb24oKSB7XG4gICAgICB2YXIgZWwgPSAkKHRoaXMpXG4gICAgICBpZiAoZWwuaXMoXCJbZGF0YS1hZGRdXCIpKSB7XG4gICAgICAgIGFkZChlbClcbiAgICAgIH1cbiAgICB9LFxuICAgIGNsaWNrOiBmdW5jdGlvbigpIHtcbiAgICAgIHZhciBlbCA9ICQodGhpcylcbiAgICAgIGlmIChlbC5pcyhcIltkYXRhLXVwZGF0ZV1cIikpIHtcbiAgICAgICAgdXBkYXRlKGVsKVxuICAgICAgfVxuICAgIH1cbiAgfSlcbn1cblxuY29uc3QgQ2hhcnRzID0ge1xuICBzZXR0aW5ncyxcbiAgaW5pdCxcbiAgYWRkLFxuICB1cGRhdGUsXG4gIGNyZWF0ZVxufVxuXG5pZiAod2luZG93ICE9PSB1bmRlZmluZWQpIHtcbiAgd2luZG93LkNoYXJ0cyA9IENoYXJ0c1xufSJdLCJzb3VyY2VSb290IjoiIn0=