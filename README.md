# Chinbi Robotics

Responsive, accessible company landing page for the Chinbi quadruped development project. The deployable website is in `dist/`; no build dependencies are required.

Preview: `python3 -m http.server 4173 --directory dist` and open http://localhost:4173.

The model specifications and CAD image come from the local CHINBI_URDF_V1_TF description: 12 actuated joints, 13 links, and 27.251 kg modeled mass. These are development model values, not measured production specifications. The site does not claim validated speed, payload, battery life, commercial readiness, or customers.

The website uses DM Sans and Manrope through Google Fonts, with system font fallbacks. Navigation and content work without JavaScript on desktop; mobile navigation uses a small dependency-free script.

The hero artwork is AI-generated illustrative concept art, visibly labeled on the page; it is not a photograph or exact rendering of the actual Chinbi prototype. Generated once using the built-in imagegen tool with the prompt: “Photorealistic industrial design concept of a research quadruped robot; silver machined aluminum skeletal chassis, black cylindrical joint motors, four articulated slender legs with rubber feet, modest orange cable accents; dark charcoal studio, three-quarter view, entire robot visible, soft white edge lighting. No face, humanoid features, text, logos, UI, or watermark.” Asset: `dist/assets/quadruped-concept.png`.

The site also includes real photographs of the hardware and team (leg assembly, CAD review, actuator assembly/testing, and a founder portrait), sourced from project materials and resized/compressed for the web. These are not AI-generated.

The page covers the platform, engineering approach, development traction, technology/IP ownership, market opportunity, business model, competitive position, financial projections, founder/team background, and an investor section (the ask, use of funds, and contact) — all bilingual (EN/VN) via `dist/i18n.js`.

The brand mark (`dist/assets/chinbi-wolf.png`) is the wolf head from the official Chinbi Robotics logo, cropped without the wordmark and kept in its original colours (black mane, white face) with the area outside the silhouette made transparent. It is used in the header and footer. A single-tone copy (`chinbi-wolf-watermark.png`) sits as a faint watermark behind the vision section. The browser-tab icon (`favicon.svg`, plus `apple-touch-icon.png`) is a simple stylised "C" in the accent colour, which stays legible at 16px.
