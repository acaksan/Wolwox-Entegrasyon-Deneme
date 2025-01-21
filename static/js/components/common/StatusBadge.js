export default {
    name: 'StatusBadge',
    props: {
        status: {
            type: String,
            required: true
        }
    },
    computed: {
        badgeClass() {
            return {
                'development': 'bg-yellow-500',
                'completed': 'bg-green-500',
                'planned': 'bg-gray-500'
            }[this.status] || 'bg-gray-500'
        },
        badgeText() {
            return {
                'development': 'Yapım Aşamasında',
                'completed': 'Hazır',
                'planned': 'Planlanıyor'
            }[this.status] || this.status
        }
    },
    template: `
        <span class="float-right text-xs text-white px-2 py-1 rounded" :class="badgeClass">
            {{ badgeText }}
        </span>
    `
} 