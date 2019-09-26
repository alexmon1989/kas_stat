<template>
    <b-container fluid>
        <params-form v-on:send-date-form="onShowStatistics"></params-form>

        <div v-if="registry && dateFrom && dateTo" class="mt-4">
            <registration-preparing :date-from="dateFrom"
                                    :date-to="dateTo"
                                    v-if="registry === 'За підготовку до державної реєстрації'"
            ></registration-preparing>

            <certificates-issues :date-from="dateFrom"
                                 :date-to="dateTo"
                                 v-if="registry === 'За видачу свідоцтв'"
            ></certificates-issues>

            <contracts-registration :date-from="dateFrom"
                                    :date-to="dateTo"
                                    v-if="registry === 'За державну реєстрацію договорів'"
            ></contracts-registration>

            <dublicates :date-from="dateFrom"
                        :date-to="dateTo"
                        v-if="registry === 'За видачу дубліката свідоцтва'"
            ></dublicates>

            <changes :date-from="dateFrom"
                     :date-to="dateTo"
                     v-if="registry === 'За внесення змін'"
            ></changes>
        </div>
    </b-container>
</template>

<script>
    import ParamsForm from './Form.vue';
    import RegistrationPreparing from './RegistrationPreparing.vue';
    import CertificatesIssues from './CertificatesIssues.vue';
    import ContractsRegistration from './ContractsRegistration.vue';
    import Dublicates from './Dublicates.vue';
    import Changes from './Changes.vue';

    export default {
        data() {
            return {
                registry: '',
                dateFrom: '',
                dateTo: '',
            }
        },

        components: {
            ParamsForm,
            CertificatesIssues,
            ContractsRegistration,
            Dublicates,
            Changes,
            RegistrationPreparing,
        },

        methods: {
            onShowStatistics: function (dateFrom, dateTo, registry) {
                this.dateFrom = dateFrom;
                this.dateTo = dateTo;
                this.registry = registry;
            }
        },
    }
</script>

<style scoped>

</style>