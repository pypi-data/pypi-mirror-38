var wsScheme = 'ws';
if (window.location.protocol == 'https:') {
  wsScheme = 'wss';
}
var wsLocation = wsScheme + "://" + window.location.host + "/websocket";

Vue.use(VueNativeSock.default, wsLocation, {
    format: 'json',
    reconnection: true
});
Vue.use(VueRouter);

Vue.component('watcher', {
  props: ['watcher'],
  template: `
<li
    class="list-group-item"
    v-bind:class="{'bg-danger': watcher.status == 'critical'}">
    <router-link 
        :to="{name: 'watcher-detail', params: {'uuid': watcher.uuid}}"
        v-bind:class="{ 'text-info': watcher.status == 'unknown', 'text-info': watcher.status == null, 'text-success': watcher.status == 'info', 'text-warning': watcher.status == 'warning', 'text-danger': watcher.status == 'error', 'text-light': watcher.status == 'critical'}"
    >
        {{ watcher.description }}
    </router-link>
</li>`
});

Vue.component('server', {
  props: ['server', 'watchers'],
  template: `
<div class="col">
<div class="card">
    <div class="card-header">
      {{ server.name }}
    </div>
    <ul class="list-group list-group-flush">
      <watcher
        v-for="watcher in watchers"
        :key="watcher.uuid"
        v-bind:watcher="watcher"></watcher>
    </ul>
</div>
</div>
`})

const WatchersList = Vue.component('watchers_list', {
  props: ['watchers'],
  template: `
<div class="row">
    <server
        v-for="(object, uuid) in by_servers"
        v-bind:server="object.server"
        v-bind:watchers="object.watchers"></server>
</div>`,
  computed: {
    by_servers: function() {
      return this.watchers.reduce(function(servers, watcher){
        if (!(watcher.server.uuid in servers)){
          servers[watcher.server.uuid] = {
            server: watcher.server,
            watchers: []
          }
        }
        servers[watcher.server.uuid].watchers.push(watcher);
        return servers;
      }, {});
    }
  }
});

const WatcherDetail = Vue.component('watcher_detail', {
  props: ['watchers', 'uuid'],
  template: `
<dl v-if="watcher">
    <dt>Server</dt>
    <dd>{{ watcher.server.name }}</dd>
    <dt>Service</dt>
    <dd>{{ watcher.description }}</dd>
    <dt>Status</dt>
    <dd v-bind:class="{ 'text-info': watcher.status == 'unknown', 'text-info': watcher.status == null, 'text-success': watcher.status == 'info', 'text-warning': watcher.status == 'warning', 'text-danger': watcher.status == 'error', 'text-light': watcher.status == 'critical', 'bg-danger': watcher.status == 'critical'}">
        {{ watcher.status }}
    </dd>
    <dt>Next check</dt>
    <dd>
      {{ next_check }}
      (<a href class="text-primary" @click.prevent="check_now">check now</a>)
    </dd>
    <dt v-if="watcher.last_result">Last result</dt>
    <dd v-if="watcher.last_result">
        <dl class="ml-4">
        <dt>Is hard</dt>
        <dd>{{ watcher.last_result.is_hard}}</dd>
        <dt>Start</dt>
        <dd>{{ watcher.last_result.start}}</dd>
        <dt>End</dt>
        <dd>{{ watcher.last_result.end}}</dd>
        <dt>Duration</dt>
        <dd>{{ duration }} ms</dd>

        <dt>Response</dt>
        <dd>
        <dl class="ml-4" v-for="(value, key) in watcher.last_result.response">
            <dt>{{ key }}</dt>
            <dd>{{ value }}</dd>
        </dl>
        </dd>
        </dl>
    </dd>
</dl>
<p v-else>Watcher not found</p>`,
  data: function(){
    return {now: Date.now(), interval_id: null}
  },
  computed: {
    watcher: function(){
      for (var i in this.watchers){
        var watcher = this.watchers[i];
        if(watcher.uuid == this.uuid){
            return watcher;
        }
      }
      return null;
    },
    duration: function(){
        if (this.watcher && this.watcher.last_result && this.watcher.last_result.start && this.watcher.last_result.end) {
        var start = new Date(this.watcher.last_result.start);
        var end = new Date(this.watcher.last_result.end);
        return end - start;
        }
        return null;
    },
    next_check: function(){
        if (this.watcher && this.watcher.next_check_hour){
            var check_hour = new Date(this.watcher.next_check_hour);
            var seconds = parseInt((check_hour - this.now) / 1000);
            if (seconds <= 0) return "checking";
            return seconds + ' seconds';
        }
        return null;
    }
  },
  mounted: function(){
    this.refresh_now();
  },
  beforeDestroy () {
    clearInterval(this.interval_id)
  },
  methods: {
    refresh_now: function(){
        this.interval_id = setInterval(function(){
          this.now = Date.now();
        }.bind(this), 1000);
    },
    check_now: function(){
        axios.get('/api/watchers/' + this.uuid + '/check_now/');
    }
  }
})

const router = new VueRouter({routes: [
    {path: '/', component: WatchersList},
    {path: '/watchers/:uuid', component: WatcherDetail, props: true, name: 'watcher-detail'}
]});

var app = new Vue({
  router: router,
  el: '#app',
  template: `
<div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light rounded mb-2">
      <a class="navbar-brand" href="#/">WatchGhost <small v-if="! ws_is_connected">(Disconnected)</small></a>
    </nav>

    <router-view :watchers="watchers" />
</div>
  `,
  data: {
    watchers: [],
    ws_is_connected: false
  },
  mounted() {
    this.ws_is_connected = this.$options.sockets.readyState == 1;
    this.$options.sockets.onopen = function(){
        this.ws_is_connected = true;
    }
    this.$options.sockets.onclose = function(){
        this.ws_is_connected = false;
        for(var i in this.watchers){
            var watcher = this.watchers[i];
            watcher.status = 'unknown';
            delete watcher.last_result;
            delete watcher.next_check_hour;
        }
    }
    axios.get('/api/watchers/').then(response => {
      this.watchers = response.data.objects;
      this.$options.sockets.onmessage = (data) => {
        this.ws_is_connected = true;
        var message = JSON.parse(data.data);
        var data_uuid = Object.keys(message)[0];
        for (var i in this.watchers){
          var watcher = this.watchers[i];
          if(watcher.uuid == data_uuid){
            var new_watcher = JSON.parse(message[data_uuid]);
            this.watchers[i].status = new_watcher.status;
            this.watchers[i].next_check_hour = new_watcher.next_check_hour;
            this.watchers[i].last_result = new_watcher.last_result;
          }
        }
      };
    });
  },
})
