<template>
    <div class="text-center">
        <h5>{{ appTableHeaderTitle }}</h5>
    </div>
</template>

<script>
    export default {
        props: ['region', 'obj_type', 'legal_type', 'dateFrom', 'dateTo'],
        computed: {
            appTableHeaderTitle() {
                let title = 'Перелік осіб, які подали заявку (регіон: ' + this.region + ', вид об\'єкта: ';

                if (this.obj_type === 'ap') {
                    title += 'АП, '
                }
                else if (this.obj_type === 'dg') {
                    title += 'ДГ, '
                }

                if (this.legal_type === 'phys') {
                    title += 'фізичні особи)'
                } else {
                     title += 'юридичні особи)'
                }
                return title;
            },
        }
    }
</script>

<style scoped>

</style>