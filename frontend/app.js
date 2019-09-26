import 'es6-promise/auto';
import 'babel-polyfill';
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'

import ap from './components/AP/AP.vue'
import dg from './components/DG/DG.vue'
import ApSpecialistWorkload from './components/ApSpecialistWorkload/ApSpecialistWorkload.vue'
import DgSpecialistWorkload from './components/DgSpecialistWorkload/DgSpecialistWorkload.vue'
import Regions from './components/Regions/Regions.vue'
import Finances from './components/Finances/Finances.vue'
import ObjTypes from './components/ObjTypes/ObjTypes.vue'
import AdminServices from './components/AdminServices/AdminServices.vue'
import Duplicates from './components/Duplicates/Duplicates.vue'

Vue.use(BootstrapVue);
Vue.use(require('vue-moment'));

const app = new Vue({
    el: '#app',
    components: {
        ap,
        dg,
        ApSpecialistWorkload,
        DgSpecialistWorkload,
        Regions,
        Finances,
        ObjTypes,
        AdminServices,
        Duplicates,
    }
});