<template>
    <b-container fluid>
        <date-form v-on:send-date-form="onShowStatistics"></date-form>

        <statistics-table v-if="dateFrom && dateTo"
                          v-on:show-apps="onShowApps"
                          :date-from="dateFrom"
                          :date-to="dateTo"
                          :app-type="appType"
        ></statistics-table>

        <div v-if="appType">
            <applications-table-header-title
                    class="mt-5"
                    :app-type="appType"
                    v-on:close-app-table="onHideApps"
            ></applications-table-header-title>
            <applications-table
                    class="mt-3"
                    :app-type="appType"
                    :date-from="dateFrom"
                    :date-to="dateTo"
            ></applications-table>
        </div>
    </b-container>
</template>

<script>
    import StatisticsTable from './StatisticsTable.vue';
    import ApplicationsTable from './ApplicationsTable.vue';
    import ApplicationsTableHeaderTitle from './ApplicationsTableHeaderTitle.vue';
    import DateForm from './DateForm.vue';

    export default {
        data() {
            return {
                appType: '',
                dateFrom: '',
                dateTo: '',
            }
        },

        components: {
            StatisticsTable,
            ApplicationsTable,
            ApplicationsTableHeaderTitle,
            DateForm
        },

        methods: {
            onShowApps: function (appType) {
                this.appType = appType;
            },

            onShowStatistics: function (dateFrom, dateTo) {
                this.dateFrom = '';
                this.dateTo = '';
                this.appType = '';

                this.$nextTick(function () {
                    this.dateFrom = dateFrom;
                    this.dateTo = dateTo;
                });
            },

            onHideApps: function () {
                this.appType = '';
            }
        },
    }
</script>