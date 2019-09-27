export default {
    methods: {
        onKeyUp(e) {
            if (e.which === 13) {
                this.$emit('send-date-form', this.from, this.to);
            }
        }
    },

    created() {
        window.addEventListener('keyup', this.onKeyUp);
    },

    beforeDestroy() {
        window.removeEventListener('keyup', this.onKeyUp);
    }
}
