<template>
    <div>
        <div class="d-flex justify-content-center mt-5" v-if="isBusy">
            <strong>Завантаження даних...</strong>
            <b-spinner class="ml-2"></b-spinner>
        </div>

        <b-table-simple small caption-top responsive striped bordered v-else>
            <caption>Статистичні дані щодо розгляду заявок на реєстрацію ДГ:</caption>
            <b-thead class="text-center">
                <b-tr>
                    <b-th rowspan="3">Вид договору</b-th>
                    <b-th rowspan="3">Сторона договору, яка подала заявку</b-th>
                    <b-th colspan="6">Заявок</b-th>
                </b-tr>
                <b-tr>
                    <b-th>подано</b-th>
                    <b-th colspan="6">розглянуто</b-th>
                </b-tr>
                <b-tr>
                    <b-th></b-th>
                    <b-th>Зареєстровано</b-th>
                    <b-th>Без розгляду</b-th>
                    <b-th>Відмова</b-th>
                    <b-th>Повернено</b-th>
                    <b-th>ВСЬОГО</b-th>
                </b-tr>
            </b-thead>
            <b-tbody class="text-center">
                <b-tr>
                    <b-td rowspan="2">Передача (відчуження)</b-td>
                    <b-td>Фізичні особи</b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'alienation_applied_phys')">{{ statistics.alienation_applied_phys }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'alienation_registered_phys')">{{ statistics.alienation_registered_phys }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'alienation_without_review_phys')">{{ statistics.alienation_without_review_phys }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'alienation_refusal_phys')">{{ statistics.alienation_refusal_phys }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'alienation_return_phys')">{{ statistics.alienation_return_phys }}</a></b-td>
                    <b-td>{{ considered_alienation_phys_sum }}</b-td>
                </b-tr>
                <b-tr>
                    <b-td>Юридичні особи</b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'alienation_applied_jur')">{{ statistics.alienation_applied_jur }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'alienation_registered_jur')">{{ statistics.alienation_registered_jur }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'alienation_without_review_jur')">{{ statistics.alienation_without_review_jur }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'alienation_refusal_jur')">{{ statistics.alienation_refusal_jur }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'alienation_return_jur')">{{ statistics.alienation_return_jur }}</a></b-td>
                    <b-td>{{ considered_alienation_jur_sum }}</b-td>
                </b-tr>
                <b-tr>
                    <b-td rowspan="2">Передача на використання</b-td>
                    <b-td>Фізичні особи</b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'using_applied_phys')">{{ statistics.using_applied_phys }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'using_registered_phys')">{{ statistics.using_registered_phys }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'using_without_review_phys')">{{ statistics.using_without_review_phys }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'using_refusal_phys')">{{ statistics.using_refusal_phys }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'using_return_phys')">{{ statistics.using_return_phys }}</a></b-td>
                    <b-td>{{ considered_using_phys_sum }}</b-td>
                </b-tr>
                <b-tr>
                    <b-td>Юридичні особи</b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'using_applied_jur')">{{ statistics.using_applied_jur }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'using_registered_jur')">{{ statistics.using_registered_jur }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'using_without_review_jur')">{{ statistics.using_without_review_jur }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'using_refusal_jur')">{{ statistics.using_refusal_jur }}</a></b-td>
                    <b-td><a href="#" @click.prevent="$emit('show-apps', 'using_return_jur')">{{ statistics.using_return_jur }}</a></b-td>
                    <b-td>{{ considered_using_jur_sum }}</b-td>
                </b-tr>
                <b-tr>
                    <b-td></b-td>
                    <b-td>Всього</b-td>
                    <b-td>{{ applied_sum }}</b-td>
                    <b-td>{{ registered_sum }}</b-td>
                    <b-td>{{ without_review_sum }}</b-td>
                    <b-td>{{ refusal_sum }}</b-td>
                    <b-td>{{ return_sum }}</b-td>
                    <b-td>{{ considered_sum }}</b-td>
                </b-tr>
            </b-tbody>
            <b-tfoot>
                <b-tr>
                    <b-td colspan="9" variant="secondary" class="text-right">
                        <b-button size="sm">Експорт у Excel</b-button>
                    </b-td>
                </b-tr>
            </b-tfoot>
        </b-table-simple>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        props: ['dateFrom', 'dateTo'],

        data() {
            return {
                isBusy: true,
                statistics: {
                    alienation_applied_phys: 0,
                    alienation_applied_jur: 0,
                    using_applied_phys: 0,
                    using_applied_jur: 0,

                    alienation_registered_phys: 0,
                    alienation_registered_jur: 0,
                    using_registered_phys: 0,
                    using_registered_jur: 0,

                    alienation_without_review_phys: 0,
                    alienation_without_review_jur: 0,
                    using_without_review_phys: 0,
                    using_without_review_jur: 0,

                    alienation_refusal_phys: 0,
                    alienation_refusal_jur: 0,
                    using_refusal_phys: 0,
                    using_refusal_jur: 0,

                    alienation_return_phys: 0,
                    alienation_return_jur: 0,
                    using_return_phys: 0,
                    using_return_jur: 0,
                },
            }
        },
        computed: {
            // Всього поданих
            applied_sum() {
                return this.statistics.alienation_applied_phys
                    + this.statistics.alienation_applied_jur
                    + this.statistics.using_applied_phys
                    + this.statistics.using_applied_jur;
            },

            // Всього зареєстровано
            registered_sum() {
                return this.statistics.alienation_registered_phys
                    + this.statistics.alienation_registered_jur
                    + this.statistics.using_registered_phys
                    + this.statistics.using_registered_jur;
            },

            // Всього без розгляду
            without_review_sum() {
                return this.statistics.alienation_without_review_phys
                    + this.statistics.alienation_without_review_jur
                    + this.statistics.using_without_review_phys
                    + this.statistics.using_without_review_jur;
            },

            // Всього відмова
            refusal_sum() {
                return this.statistics.alienation_refusal_phys
                    + this.statistics.alienation_refusal_jur
                    + this.statistics.using_refusal_phys
                    + this.statistics.using_refusal_jur;
            },

            // Всього повернено
            return_sum() {
                return this.statistics.alienation_return_phys
                    + this.statistics.alienation_return_jur
                    + this.statistics.using_return_phys
                    + this.statistics.using_return_jur;
            },

            // Всього розглянуто фіз. (відчуження)
            considered_alienation_phys_sum() {
                return this.statistics.alienation_registered_phys
                    + this.statistics.alienation_without_review_phys
                    + this.statistics.alienation_refusal_phys
                    + this.statistics.alienation_return_phys;
            },

            // Всього розглянуто фіз. (використання)
            considered_using_phys_sum() {
                return this.statistics.using_registered_phys
                    + this.statistics.using_without_review_phys
                    + this.statistics.using_refusal_phys
                    + this.statistics.using_return_phys;
            },

            // Всього розглянуто юр. (відчуження)
            considered_alienation_jur_sum() {
                return this.statistics.alienation_registered_jur
                    + this.statistics.alienation_without_review_jur
                    + this.statistics.alienation_refusal_jur
                    + this.statistics.alienation_return_jur;
            },

            // Всього розглянуто юр. (використання)
            considered_using_jur_sum() {
                return this.statistics.using_registered_jur
                    + this.statistics.using_without_review_jur
                    + this.statistics.using_refusal_jur
                    + this.statistics.using_return_jur;
            },

            // Всього розглянуто
            considered_sum() {
                return this.considered_alienation_phys_sum
                    + this.considered_using_phys_sum
                    + this.considered_alienation_jur_sum
                    + this.considered_using_jur_sum;
            }
        },

        created() {
            // Загрузка статистических данных
            this.getStatisticsData();
        },

        methods: {
            getStatisticsData: function () {
                this.isBusy = true;
                axios.get('/api/statistics/dg/', {
                    params: {
                        date_from: this.dateFrom.toISOString().split('T')[0],
                        date_to: this.dateTo.toISOString().split('T')[0],
                    }
                }).then(response => {
                    this.statistics = response.data;
                    this.isBusy = false;
                })
            }
        },

        watch: {
            dateFrom() {
                if (!this.isBusy) {
                    this.getStatisticsData();
                }
            },
            dateTo() {
                if (!this.isBusy) {
                    this.getStatisticsData();
                }
            }
        }
    }
</script>