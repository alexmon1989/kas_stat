<template>
    <b-container fluid>
        <date-form v-on:send-date-form="onShowStatistics"></date-form>

        <statistics-table v-if="dateFrom && dateTo"
                          v-on:show-apps="onShowApps"
                          :date-from="dateFrom"
                          :date-to="dateTo"
                          :app-type="appType"
                          :obj-type="objType"
        ></statistics-table>

        <div v-if="appType && objType">
            <div class="d-flex justify-content-between mt-5">
                <h5>Перелік заявок</h5>
                <b-button pill
                          variant="outline-danger"
                          size="sm"
                          @click="onHideApps()"
                >&times; Закрити</b-button>
            </div>

            <applications-table
                    class="mt-3"
                    :app-type="appType"
                    :obj-type="objType"
                    :date-from="dateFrom"
                    :date-to="dateTo"
            ></applications-table>
        </div>
    </b-container>
</template>

<script>
    import DateForm from './DateForm.vue';
    import StatisticsTable from './StatisticsTable.vue';
    import ApplicationsTable from './ApplicationsTable.vue';

    export default {
        data() {
            return {
                dateFrom: '',
                dateTo: '',
                appType: '',
                objType: '',
            }
        },

        components: {
            DateForm,
            StatisticsTable,
            ApplicationsTable,
        },

        methods: {
            onShowApps: function (objType, appType) {
                this.objType = objType;
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
                this.objType = '';
            }
        },
    }
</script>

<style scoped>

</style>