if (typeof lucide !== "undefined") {
  lucide.createIcons();
}

function setupRadioCards(
  groupSelector,
  itemSelector,
  activeClasses,
  inactiveClasses,
) {
  const radios = document.querySelectorAll(
    `${groupSelector} input[type="radio"]`,
  );
  radios.forEach((radio) => {
    radio.addEventListener("change", () => {
      document.querySelectorAll(itemSelector).forEach((label) => {
        label.classList.remove(...activeClasses);
        label.classList.add(...inactiveClasses);
      });
      const parent = radio.closest(itemSelector);
      parent.classList.remove(...inactiveClasses);
      parent.classList.add(...activeClasses);
    });
  });
}

setupRadioCards(
  "#location-type-group",
  ".location-option",
  ["border-indigo-500", "bg-indigo-50/50", "text-indigo-700", "font-semibold"],
  ["border-slate-200", "bg-white", "text-slate-600", "font-medium"],
);
setupRadioCards(
  "#ticket-type-group",
  ".ticket-option",
  ["border-indigo-500", "bg-indigo-50/50", "text-indigo-700", "font-semibold"],
  ["border-slate-200", "bg-white", "text-slate-600", "font-medium"],
);
setupRadioCards(
  "#visibility-group",
  ".visibility-option",
  ["border-slate-300", "bg-slate-50/70"],
  ["border-transparent"],
);

document.querySelectorAll('input[name="ticket_type"]').forEach((radio) => {
  radio.addEventListener("change", (e) => {
    const priceWrapper = document.getElementById("ticket-price-wrapper");
    priceWrapper.classList.toggle("hidden", e.target.value !== "paid");
  });
});

const fileInput = document.getElementById("cover_image");
fileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (file) {
    document.getElementById("upload-placeholder").classList.add("hidden");
    const preview = document.getElementById("file-name-preview");
    preview.textContent = `Selected: ${file.name}`;
    preview.classList.remove("hidden");
  }
});

function updateChecklist() {
  const checks = {
    "check-essentials":
      document.getElementById("title").value.trim() &&
      document.getElementById("category").value &&
      document.getElementById("description").value.trim().length >= 50,
    "check-schedule":
      document.getElementById("start_date").value &&
      document.getElementById("start_time").value &&
      document.getElementById("venue_name").value.trim(),
    "check-registration": document.getElementById("max_attendees").value > 0,
    "check-organizer":
      document.getElementById("organizer_name").value.trim() &&
      document.getElementById("contact_email").value.includes("@"),
  };

  for (const [id, isComplete] of Object.entries(checks)) {
    const dot = document.querySelector(`#${id} .status-dot`);
    if (isComplete) {
      dot.className =
        "status-dot w-4 h-4 rounded-full bg-emerald-500 text-white mt-0.5 shrink-0 flex items-center justify-center text-[10px]";
      dot.innerHTML = "✓";
    } else {
      dot.className =
        "status-dot w-4 h-4 rounded-full border border-slate-300 mt-0.5 shrink-0 flex items-center justify-center";
      dot.innerHTML = "";
    }
  }
}

document.querySelectorAll("input, select, textarea").forEach((el) => {
  el.addEventListener("input", updateChecklist);
  el.addEventListener("change", updateChecklist);
});
