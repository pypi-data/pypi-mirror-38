// shortcut - if you paste the full chessgames
// game url into the field it will extract the ID

django.jQuery(document).ready(() => {
  document.querySelectorAll('.field-chessgames_id input').forEach(el => {
    el.addEventListener('change', () => {
      const v = el.value
      if (v.includes("http")) {
        const url = new URL(v)
        el.value = url.searchParams.get('gid')
      }
    })
  })
})
