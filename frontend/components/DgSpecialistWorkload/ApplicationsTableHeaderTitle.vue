<template>
    <div class="d-flex justify-content-between">
        <h5>{{ appTableHeaderTitle }}</h5>
        <b-button pill
                  variant="outline-danger"
                  size="sm"
                  @click="$emit('close-app-table')"
        >&times; Закрити</b-button>
    </div>
</template>

<script>
    export default {
        props: ['appType', 'specialistName'],
        computed: {
            appTableHeaderTitle() {
                let title = '';

                if (this.appType === 'applied') {
                    title = 'Список прийнятих до розгляду заявок фахівцем '
                }
                else if (this.appType === 'reviewed') {
                    title = 'Список розглянутих заявкок фахівцем '
                } else {
                     title = 'Список заявкок фахівця '
                }

                title = title + this.specialistName;

                return title;
            },
        }
    }
</script>

<style scoped>

</style>