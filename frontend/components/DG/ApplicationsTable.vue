<template>
    <div>
        <b-table :items="getItems"
                 :fields="fields"
                 striped
                 responsive="sm"
                 empty-text="Заявки відсутні"
                 show-empty
                 :current-page="currentPage"
                 :per-page="perPage"
                 ref="table"
        >
            <template v-slot:table-busy>
                <div class="text-center my-2">
                    <b-spinner class="align-middle"></b-spinner>
                    <strong>Завантаження даних...</strong>
                </div>
            </template>

            <template v-slot:cell(app_number)="row">
                <a href="#" @click.prevent="row.toggleDetails">{{ row.item.claim_number || '-' }}</a>
            </template>

            <template v-slot:cell(subject)="row">
                {{ getPerson(row.item) }}
            </template>

            <template v-slot:cell(object)="row">
                {{ getObject(row.item) }}
            </template>

            <template v-slot:row-details="row">
                <app-details :app="row.item"></app-details>
            </template>
        </b-table>

        <b-row class="justify-content-center" v-if="totalRows > perPage">
            <b-col sm="7" md="6" class="my-1">
                <b-pagination v-model="currentPage"
                              :total-rows="totalRows"
                              :per-page="perPage"
                              align="fill"
                ></b-pagination>
            </b-col>
        </b-row>
    </div>
</template>

<script>
    import axios from 'axios';
    import AppDetails from './AppDetails.vue';

    export default {
        props: ['appType', 'dateFrom', 'dateTo'],
        components: {
            AppDetails
        },
        data() {
            return {
                fields: [
                    {key: 'app_number', label: '№ заявки'},
                    {key: 'subject', label: 'Сторона договору, яка подає заявку'},
                    {key: 'object', label: 'Об\'єкт(и) АП, на які передаються права'},
                ],
                totalRows: 1,
                currentPage: 1,
                perPage: 10,
            }
        },
        watch: {
            appType() {
                this.totalRows = 1;
                this.currentPage = 1;
                this.$refs.table.refresh();
            }
        },
        methods: {
            // Получение списка заявок с сервера
            getItems(ctx) {
                let promise = axios.get('/api/dg_claims/', {
                    params: {
                        appType: this.appType,
                        date_from: this.dateFrom.toISOString().split('T')[0],
                        date_to: this.dateTo.toISOString().split('T')[0],
                        page: ctx.currentPage,
                    }
                });
                return promise.then((response) => {
                    this.totalRows = response.data.count;
                    return(response.data.results || []);
                });
            },

            getPerson(app) {
                if (!app.persons.length) {
                    return '-';
                }
                return app.persons[0]['full_name'];
            },

            getObject(app) {
                if (!app.oap.length) {
                    return '-';
                }
                return app.oap.map(function (item) {
                    return item.oap_name
                }).join(';')
            }
        }
    }
</script>