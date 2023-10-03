import { Desktop } from 'Windows'
import { Wallpaper } from 'Wallhaven'

function startDesktop() {
    Desktop.setOptions({
        mode: 'clean',
        background: Wallpaper,
    })

    Desktop.initialize()
}

startDesktop()