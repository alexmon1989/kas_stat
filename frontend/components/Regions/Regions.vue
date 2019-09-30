<template>
    <b-container fluid>
        <date-form v-on:send-date-form="onShowStatistics"></date-form>

        <statistics-table v-if="dateFrom && dateTo"
                          v-on:show-apps="onShowApps"
                          :date-from="dateFrom"
                          :date-to="dateTo"
                          :region="region"
                          :obj_type="obj_type"
                          :legal_type="legal_type"
        ></statistics-table>

        <div v-if="region">
            <persons-table-header-title
                    class="mt-5"
                    :region="region"
                    :obj_type="obj_type"
                    :legal_type="legal_type"
                    v-on:close-persons-table="onHidePersons"
            ></persons-table-header-title>
            <persons-table
                    class="mt-3"
                    :region="region"
                    :obj_type="obj_type"
                    :legal_type="legal_type"
                    :date-from="dateFrom"
                    :date-to="dateTo"
            ></persons-table>
        </div>
    </b-container>
</template>

<script>
    import DateForm from './DateForm.vue';
    import StatisticsTable from './StatisticsTable.vue';
    import PersonsTable from './PersonsTable.vue';
    import PersonsTableHeaderTitle from './PersonsTableHeaderTitle.vue';

    export default {
        components: {
            PersonsTableHeaderTitle,
            DateForm,
            StatisticsTable,
            PersonsTable,
        },

        data() {
            return {
                dateFrom: '',
                dateTo: '',
                region: '',
                obj_type: '',
                legal_type: '',
            }
        },

        methods: {
            onShowApps: function (region, obj_type, legal_type) {
                this.region = region;
                this.obj_type = obj_type;
                this.legal_type = legal_type;
            },

            onShowStatistics: function (dateFrom, dateTo) {
                this.region = '';
                this.dateFrom = '';
                this.dateTo = '';

                this.$nextTick(function () {
                    this.dateFrom = dateFrom;
                    this.dateTo = dateTo;
                });
            },

            onHidePersons: function () {
                this.region = '';
            }
        },
    }
</script>

<style scoped>

</style>