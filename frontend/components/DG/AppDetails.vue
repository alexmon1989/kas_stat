<template>
    <div>
        <b-table :fields="fields" :items="items" small></b-table>

        <div class="mt-3 d-flex justify-content-end">
            <b-link class="btn btn-primary" :href="href" target="_blank"><i class="fa fa-external-link mr-2"></i>Бібліографічні дані заявки</b-link>
        </div>
    </div>
</template>

<script>
    export default {
        name: "AppDetails",
        props: ['app'],
        data() {
            return {
                fields: [
                    {key: 'professional_name', label: 'ФІО фахівця'},
                    {key: 'receive_date', label: 'Дата отримання'},
                    {key: 'stage', label: 'Етап розгляду заявки'},
                    {key: 'stage_finish_date', label: 'Дата завершення етапу'},
                ],
                items: []
            }
        },
        mounted() {
            this.items = this.app.events.map(function (item) {
                let user = '-';
                if (item.user !== null) {
                    user = [item.user.last_name, item.user.first_name, item.user.middle_name].join(' ');
                }
                return {
                    'professional_name': user,
                    'receive_date': new Date(item.event_date).toLocaleDateString(),
                    'stage': item.event_type.event_name,
                    'stage_finish_date': new Date(item.event_date).toLocaleDateString(),
                }
            });
        },
        computed: {
            href() {
                return '//spec.authors.ukrpatent.org/claims/claim?id=' + this.app.idclaim;
            }
        }
    }
</script>

<style scoped>

</style>