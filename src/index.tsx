import {
  ButtonItem,
  PanelSection,
  PanelSectionRow,
  staticClasses,
  ToggleField,
  SliderField,
} from "@decky/ui";
import { callable, definePlugin } from "@decky/api";
import { FaLightbulb } from "react-icons/fa";
import { useEffect, useState } from "react";

const toggleHue = callable<[], any>("toggle_hue");
const getHyperHdrInfo = callable<[], any>("get_hyperhdr_info");
const setHdr = callable<[number], any>("set_hdr");
const setBrightness = callable<[number], any>("set_brightness");

function Content() {
  const [hdrEnabled, setHdrEnabled] = useState<boolean>(false);
  const [brightness, setBrightnessState] = useState<number>(100);

  useEffect(() => {
    getHyperHdrInfo().then((res) => {
      if (res && res.info) {
        setHdrEnabled(res.info.videomodehdr === 1);
        if (res.info.adjustment && res.info.adjustment.length > 0) {
          setBrightnessState(res.info.adjustment[0].brightness);
        }
      }
    }).catch(console.error);
  }, []);

  const onClickToggleHue = async () => {
    await toggleHue();
  };

  const onToggleHdr = (value: boolean) => {
    setHdrEnabled(value);
    setHdr(value ? 1 : 0).catch(console.error);
  };

  const onChangeBrightness = (value: number) => {
    setBrightnessState(value);
    setBrightness(value).catch(console.error);
  };

  return (
    <PanelSection title="Ambilight">
      <PanelSectionRow>
        <ButtonItem layout="below" onClick={onClickToggleHue}>
          Activar / Desactivar Luces
        </ButtonItem>
      </PanelSectionRow>
      <PanelSectionRow>
        <ToggleField
          label="Modo HDR"
          checked={hdrEnabled}
          onChange={onToggleHdr}
        />
      </PanelSectionRow>
      <PanelSectionRow>
        <SliderField
          label="Brillo"
          value={brightness}
          step={1}
          max={100}
          min={1}
          onChange={onChangeBrightness}
        />
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
