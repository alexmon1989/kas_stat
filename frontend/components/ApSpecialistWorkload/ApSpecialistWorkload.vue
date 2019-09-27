<template>
    <b-container fluid>
        <date-form v-on:send-date-form="onShowStatistics"></date-form>

        <statistics-table v-if="dateFrom && dateTo"
                          v-on:show-apps="onShowApps"
                          :date-from="dateFrom"
                          :date-to="dateTo"
        ></statistics-table>

        <div v-if="showApps">
            <applications-table-header-title
                    class="mt-5"
                    :app-type="appType"
                    :specialist-name="specialistName"
                    v-on:close-app-table="onHideApps"
            ></applications-table-header-title>

            <applications-table
                    class="mt-3"
                    :app-type="appType"
                    :specialist-name="specialistName"
                    :date-from="dateFrom"
                    :date-to="dateTo"
            ></applications-table>
        </div>
    </b-container>
</template>

<script>
    import DateForm from './DateForm.vue';
    import StatisticsTable from './StatisticsTable.vue';
    import ApplicationsTableHeaderTitle from './ApplicationsTableHeaderTitle.vue';
    import ApplicationsTable from './ApplicationsTable.vue';

    export default {
        name: "ApSpecialistWorkload",

        components: {
            DateForm,
            StatisticsTable,
            ApplicationsTableHeaderTitle,
            ApplicationsTable
        },

        data() {
            return {
                dateFrom: '',
                dateTo: '',
                appType: '',
                specialistName: '',
                showApps: false,
            }
        },

        methods: {
            onShowApps: function (appType, specialistName) {
                this.appType = appType;
                this.specialistName = specialistName;
                this.showApps = true;
            },

            onShowStatistics: function (dateFrom, dateTo) {
                this.dateFrom = '';
                this.dateTo = '';

                this.$nextTick(function () {
                    this.dateFrom = dateFrom;
                    this.dateTo = dateTo;
                });
            },

            onHideApps: function () {
                this.showApps = false;
            }
        },
    }
</script>

<style scoped>

</style>