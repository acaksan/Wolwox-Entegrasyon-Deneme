import NotFound from './pages/NotFound.js'
import Dashboard from './pages/Dashboard.js'

export const routes = [
    {
        path: '/',
        component: Dashboard
    },
    {
        path: '/:pathMatch(.*)*',
        component: NotFound
    }
] 