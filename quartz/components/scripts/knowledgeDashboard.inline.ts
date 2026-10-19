document.addEventListener("nav", () => {
  for (const button of document.querySelectorAll<HTMLButtonElement>("[data-dashboard-search]")) {
    const open = () =>
      document.dispatchEvent(
        new CustomEvent("quartz:search", {
          detail: { term: button.dataset.dashboardSearch ?? "" },
        }),
      )
    button.addEventListener("click", open)
    window.addCleanup(() => button.removeEventListener("click", open))
  }
})
