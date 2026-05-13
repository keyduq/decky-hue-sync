import {
  ButtonItem,
  PanelSection,
  PanelSectionRow,
  staticClasses,
} from "@decky/ui";
import { callable, definePlugin } from "@decky/api";
import { FaLightbulb } from "react-icons/fa";

const toggleHue = callable<[], any>("toggle_hue");

function Content() {
  const onClick = async () => {
    await toggleHue();
  };

  return (
    <PanelSection title="Ambilight">
      <PanelSectionRow>
        <ButtonItem layout="below" onClick={onClick}>
          Activar / Desactivar Luces
        </ButtonItem>
      </PanelSectionRow>
    </PanelSection>
  );
}

export default definePlugin(() => {
  return {
    name: "DeckyHueSync",
    titleView: <div className={staticClasses.Title}>Decky Hue Sync</div>,
    content: <Content />,
    icon: <FaLightbulb />,
  };
});
