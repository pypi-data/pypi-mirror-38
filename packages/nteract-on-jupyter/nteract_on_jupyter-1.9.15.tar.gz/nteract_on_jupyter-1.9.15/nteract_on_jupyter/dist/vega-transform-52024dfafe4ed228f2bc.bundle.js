(window.webpackJsonp=window.webpackJsonp||[]).push([[12],{1369:function(e,t){},1874:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var o=function(e){return e&&e.__esModule?e:{default:e}}(n(1875));t.default=o.default},1880:function(e,t){},1881:function(e,t){},1882:function(e,t){},1883:function(e,t){},1994:function(e,t){},1995:function(e,t){},876:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.Vega=t.VegaLite=t.VegaEmbed=void 0;var o=function(){function e(e,t){for(var n=0;n<t.length;n++){var o=t[n];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(e,o.key,o)}}return function(t,n,o){return n&&e(t.prototype,n),o&&e(t,o),t}}();t.VegaLite1=p,t.Vega2=v,t.VegaLite2=g,t.Vega3=h;var a=function(e){if(e&&e.__esModule)return e;var t={};if(null!=e)for(var n in e)Object.prototype.hasOwnProperty.call(e,n)&&(t[n]=e[n]);return t.default=e,t}(n(1)),r=n(90),i=c(n(1874)),u=c(n(2037));function c(e){return e&&e.__esModule?e:{default:e}}var l=500,s=l/1.5;function d(e,t,n,o,a){if("vega2"==o){var c={mode:n,spec:Object.assign({},t)};"vega-lite"===n&&(c.spec.config=(0,r.merge)({cell:{width:l,height:s}},c.spec.config)),(0,i.default)(e,c,a)}else t=Object.assign({},t),"vega-lite"===n&&(t.config=(0,r.merge)({cell:{width:l,height:s}},t.config)),(0,u.default)(e,t,{mode:n,actions:!1}).then(function(e){return a(null,e)}).catch(a)}var f=t.VegaEmbed=function(e){function t(){return function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,t),function(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}(this,(t.__proto__||Object.getPrototypeOf(t)).apply(this,arguments))}return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}(t,a.Component),o(t,[{key:"componentDidMount",value:function(){this.el&&d(this.el,this.props.data,this.props.embedMode,this.props.version,this.props.renderedCallback)}},{key:"shouldComponentUpdate",value:function(e){return this.props.data!==e.data}},{key:"componentDidUpdate",value:function(){this.el&&d(this.el,this.props.data,this.props.embedMode,this.props.version,this.props.renderedCallback)}},{key:"render",value:function(){var e=this;return a.createElement(a.Fragment,null,a.createElement("style",null,".vega-actions{ display: none; }"),a.createElement("div",{ref:function(t){e.el=t}}))}}]),t}();function p(e){return a.createElement(f,{data:e.data,embedMode:"vega-lite",version:"vega2"})}function v(e){return a.createElement(f,{data:e.data,embedMode:"vega",version:"vega2"})}function g(e){return a.createElement(f,{data:e.data,embedMode:"vega-lite",version:"vega3"})}function h(e){return a.createElement(f,{data:e.data,embedMode:"vega",version:"vega3"})}f.defaultProps={renderedCallback:function(){},embedMode:"vega-lite",version:"vega2"},p.MIMETYPE="application/vnd.vegalite.v1+json",v.MIMETYPE="application/vnd.vega.v2+json",t.VegaLite=p,t.Vega=v,g.MIMETYPE="application/vnd.vegalite.v2+json",h.MIMETYPE="application/vnd.vega.v3+json"}}]);