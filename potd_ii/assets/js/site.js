/**
 * © Christoph Haunschmidt
 */
"use strict";

var KC = {
	END: 35,
	HOME: 36,
	LEFT: 37,
	UP: 38,
	RIGHT: 39,
	DOWN: 40,
};

function dlog(msg) {
	if (DEBUG) {
		console.log(msg)
	}
}

function trans(what) {
	if (window.TRANS && window.TRANS.hasOwnProperty(what)) {
		return window.TRANS[what]
	}
	return what
}

function toggleFullScreen() {
	if ((document.fullScreenElement && document.fullScreenElement !== null) ||
		(!document.mozFullScreen && !document.webkitIsFullScreen)) {
		if (document.documentElement.requestFullScreen) {
			document.documentElement.requestFullScreen();
		} else if (document.documentElement.mozRequestFullScreen) {
			document.documentElement.mozRequestFullScreen();
		} else if (document.documentElement.webkitRequestFullScreen) {
			document.documentElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);
		}
	} else {
		if (document.cancelFullScreen) {
			document.cancelFullScreen();
		} else if (document.mozCancelFullScreen) {
			document.mozCancelFullScreen();
		} else if (document.webkitCancelFullScreen) {
			document.webkitCancelFullScreen();
		}
	}
}

Vue.component('potd-detail', {
		props: ['potd'],
		template: '<article v-if="potd" class="potd-detail"><div>' +
		'<div class="header"><h1>{{ potd.title }}</h1>&nbsp; | {{ potd.potd_at }} | ' +
		'<a v-bind:href="infoURL" target="blank">{{ sourceTypeLong }}</a></div>' +
		'<p v-html="markedDescription" class="description"></p>' +
		'<p v-if="potd.copyright_info" class="credits">Credits: <span v-html="markedCopyrightInfo"></span></p>' +
		'<img v-if="potd.image" v-bind:src="potd.thumbnail_full_urls.potd1200" v-bind:alt="potd.title"></div>' +
		'<img v-if="!potd.image" src="' + STATIC_URL + 'img/placeholder.jpg" title="No image available" alt="No image available">' +
		'</article>',
		computed: {
			markedDescription: function () {
				return this.potd ? this._removeP(marked(this.potd.description)) : ''
			},
			markedCopyrightInfo: function () {
				return (this.potd && this.potd.copyright_info) ? this._removeP(marked(this.potd.copyright_info)) : ''
			},
			infoURL: function () {
				return this.potd ? (this.potd.detail_url ? this.potd.detail_url : this.potd.source_url) : ''
			},
			sourceTypeLong: function () {
				return trans(this.potd.source_type)
			}
		},
		methods: {
			_removeP: function (html) {
				return html.replace(/^\s*<p>\s*|\s*<\/p>\s*$/gm, '')
			}
		}
	}
);

new Vue({
	el: '#app',
	data: function () {
		return {
			potds: {},
			activeDate: null,
			activeSourceType: null,
			fullscreen: false,
			earliestDate: '2099-12-31',
			latestDate: '1970-01-01',
			earliestLoaded: false,
			latestLoaded: false,
			sortedPotds: [],
			initialize: true,
		}
	},
	methods: {
		toggleFullScreen: function () {
			this.fullscreen != this.fullscreen;
			toggleFullScreen()
		},
		insertOrUpdate: function (data) {
			var newPotds = data.hasOwnProperty('id') ? [data] : data;
			for (var i = 0; i < newPotds.length; i++) {
				var p = newPotds[i];
				if (!this.potds.hasOwnProperty(p.potd_at)) {
					this.potds[p.potd_at] = {}
				}
				this.potds[p.potd_at][p.source_type] = p;
				if (p.potd_at < this.earliestDate) {
					this.earliestDate = p.potd_at
				}
				if (p.potd_at > this.latestDate) {
					this.latestDate = p.potd_at
				}
			}
			this.updateSortedPotds();
			dlog("Loaded date range: " + this.earliestDate + " - " + this.latestDate);
		},
		gotoEarlierPotd: function () {
			this.step(-1)
		},
		gotoLaterPotd: function () {
			this.step(1)
		},
		canStep: function (direction) {
			var currentIndex = this.activePotdIndex;
			if (direction === -1 && currentIndex > 0) {
				return true
			}
			if (direction === 1 && currentIndex < this.sortedPotds.length - 1) {
				return true
			}
			return false
		},
		step: function (direction) {
			if (!this.canStep(direction)) {
				dlog("Cannot go in direction " + direction + " anymore");
				return
			}
			var currentIndex = this.activePotdIndex;
			var k = this.sortedPotds[currentIndex + direction].split('°');
			this.activeDate = k[0];
			this.activeSourceType = k[1];
		},
		loadPotdData: function (direction) {
			var vm = this, params = [];
			if (direction === -1) {
				if (this.initialize) {
					params.push('max_date=' + this.activeDate)
				} else {
					params.push('before_date=' + this.activeDate);
					this.initialize = false;
				}
			} else {
				params.push('after_date=' + this.activeDate)
			}
			jQuery.get('/api/v1/potds/?' + params.join('&'), function (data) {
				if (data.results.length) {
					vm.insertOrUpdate(data.results);
				} else {
					if (direction < 0) {
						vm.earliestLoaded = true
					} else {
						vm.latestLoaded = true
					}
				}
			});
		},
		updateSortedPotds: function () {
			var l = [];
			var sortedDates = Object.keys(this.potds).sort();
			for (var i = 0; i < sortedDates.length; i++) {
				var sortedSourceTypes = Object.keys(this.potds[sortedDates[i]]).sort();
				for (var j = 0; j < sortedSourceTypes.length; j++) {
					var p = this.potds[sortedDates[i]][sortedSourceTypes[j]];
					l.push(p.potd_at + '°' + p.source_type)
				}
			}
			this.sortedPotds = l;
		},
	},
	computed: {
		activePotd: function () {
			if (this.activeDate && this.activeDate in this.potds
				&& this.activeSourceType && this.activeSourceType in this.potds[this.activeDate]) {
				var potd = this.potds[this.activeDate][this.activeSourceType];
				document.title = potd.title;
				window.history.replaceState(potd, potd.title, potd.full_url);
				return potd
			} else return null;
		},
		activePotdKey: function () {
			return this.activePotd ? this.activePotd.potd_at + '°' + this.activePotd.source_type : null;
		},
		activePotdIndex: function () {
			return this.activePotd ? this.sortedPotds.indexOf(this.activePotdKey) : null;
		},
	},
	watch: {
		activePotd: function () {
			var threshold = 0;
			var aidx = this.activePotdIndex,
				amaxindx = this.sortedPotds.length - 1;
			if (aidx <= threshold && !this.earliestLoaded) {
				this.loadPotdData(-1)
			}
			if (aidx >= (amaxindx - threshold)  && !this.latestLoaded) {
				this.loadPotdData(1)
			}
		},
	},
	created: function () {
		// fugly globals, but works...
		var idata = window.initialData;
		if (idata) {
			this.insertOrUpdate(idata);
			if ('potd_at' in idata) {
				this.activeDate = idata.potd_at;
				this.activeSourceType = idata.source_type;
			}
		}
		var vm = this;
		$(document).keydown(function (e) {
			switch (e.which) {
				case KC.LEFT:
					vm.gotoLaterPotd();
					break;
				case KC.RIGHT:
					vm.gotoEarlierPotd();
					break;
				case KC.DOWN:
					vm.toggleFullScreen();
					break;
				default:
					return;
			}
			e.preventDefault();
		});
	},
});
