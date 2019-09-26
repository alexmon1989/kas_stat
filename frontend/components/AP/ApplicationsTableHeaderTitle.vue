<template>
    <div class="text-center">
        <h5>{{ appTableHeaderTitle }}</h5>
    </div>
</template>

<script>
    export default {
        props: ['appType'],
        data() {
            return {
                appTypesTitles: {
                    applied_phys: 'Список поданих заявок фізичними особами',
                    applied_jur: 'Список поданих заявок юридичними особами',
                    registered_phys: 'Список зареєстрованих заявок, поданих фізичними особами',
                    registered_jur: 'Список зареєстрованих заявок, поданих юридичними особами',
                    without_review_phys: 'Список заявок без розгляду, поданих фізичними особами',
                    without_review_jur: 'Список заявок без розгляду, поданих юридичними особами',
                    refusal_phys: 'Список заявок, поданих фізичними особами, яким відмовлено у розгляді',
                    refusal_jur: 'Список заявок, поданих юридичними особами, яким відмовлено у розгляді',
                    return_phys: 'Список повернених заявок, поданих фізичними особами',
                    return_jur: 'Список повернених заявок, поданих юридичними особами',
                    canceled_phys: 'Список відхилених заявок, поданих фізичними особами',
                    canceled_jur: 'Список відхилених заявок, поданих юридичними особами',
                    issued_phys: 'Список заявок, поданих фізичними особами, по яким видані свідоцтва',
                    issued_jur: 'Список заявок, поданих юридичними особами, по яким видані свідоцтва',
                }
            }
        },
        computed: {
            appTableHeaderTitle() {
                return this.appTypesTitles[this.appType];
            },
        }
    }
</script>

<style scoped>

</style>