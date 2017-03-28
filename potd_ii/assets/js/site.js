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
		template: '<div><h1>{{ potd.title }}</h1><p v-html="markedDescription"></p><img v-bind:src="potd.thumbnail_full_urls.potd1200" v-bind:title="imgTitle" v-bind:alt="potd.title"></div>',
		computed: {
			markedDescription: function () {
				return this.potd ? marked(this.potd.description) : ''
			},
			imgTitle: function () {
				return this.potd ? (this.potd.title + "\n" + this.potd.description) : ''
			},
		},
	}
);

Vue.component('potd-detail-controller', {
		props: ['pk'],
		template: '<div><div v-if="potd"><button class="btn" v-bind:class="{ \'btn-disabled\': !potd.neighbours.previous_id }" ' +
		'@click="previousPotd">earlier</button>' +
		'<button v-on:click="toggleFullScreen" class="btn">Fullscreen</button>' +
		'<button class="btn" @click="nextPotd">later</button>' +
		'<potd-detail v-if="potd" v-bind:potd="potd"></potd-detail>' +
		'</div></div>',
		data: function () {
			return {potd: null, current_pk: null, fullScreen: false}
		},
		watch: {
			current_pk: function (val) {
				var vm = this;
				jQuery.get('/api/v1/potds/' + val + '/', function (data) {
					vm.potd = data
				});
			},
			potd: function () {
				document.title = this.potd.title;
				// TODO: enable proper history (with pushState)
				window.history.replaceState(this.potd, this.potd.title, this.potd.full_url);
			},
		},
		methods: {
			previousPotd: function () {
				if (this.potd.neighbours.previous_id) this.current_pk = this.potd.neighbours.previous_id;
			},
			nextPotd: function () {
				if (this.potd.neighbours.next_id) this.current_pk = this.potd.neighbours.next_id;
			},
			toggleFullScreen: function () {
				this.fullScreen = !this.fullScreen;
				toggleFullScreen();
			},
		},
		created: function () {
			this.current_pk = this.pk;
			var vm = this;
			$(document).keydown(function (e) {
				switch (e.which) {
					case KC.LEFT:
						vm.previousPotd();
						break;
					case KC.RIGHT:
						vm.nextPotd();
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
	}
);

new Vue({
	el: '#app',
});
