import React from "react";
import truckyLogoUrl from "../assets/brand/trucky-logo.gif";

export default function BrandLogo({ size = "md", label = "TRUCKY logo" }) {
  return (
    <span className={`brand-logo brand-logo-${size}`} role="img" aria-label={label}>
      <img src={truckyLogoUrl} alt="" aria-hidden="true" />
    </span>
  );
}
