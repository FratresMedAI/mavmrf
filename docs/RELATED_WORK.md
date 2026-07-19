# Related work

MAVMRF is a **simulation-first lab baseline**, not a replacement for dataset papers or harbour-validated trackers. The following surveys and open resources situate the design choices (multi-modal streams, optical detect + track, fusion under uncertainty).

## Surveys (maritime multi-sensor fusion)

- [Multi-sensor data fusion in maritime surveillance: a review on methods and applications](https://peerj.com/articles/cs-3765) (PeerJ Computer Science) -- methods and application areas for multi-sensor maritime surveillance; notes YOLO + tracking as common optical paths and feature-/decision-level fusion.
- [A comprehensive review of multimodal artificial intelligence techniques in maritime surveillance using AIS, SAR, and optical data fusion](https://doi.org/10.1016/j.array.2026.100931) (*Array*) -- multimodal AIS / SAR / optical fusion trends and open challenges (heterogeneity, label sparsity, explainability).
- [AI in Maritime Security: Applications, Challenges, Future Directions, and Key Data Sources](https://www.mdpi.com/2078-2489/16/8/658) (MDPI *Information*) -- security-oriented multimodal fusion context and data-source landscape.

## Open benchmarks and validated trackers

- [Autoferry sensor fusion dataset](https://github.com/Autoferry/sensor_fusion_dataset) -- maritime multi-sensor, multi-target tracking benchmark (radar / lidar / EO / IR detections + ground truth); associated paper on heterogeneous tracking for an ASV.
- [harbour-multi-sensor-tracking](https://github.com/elifpulukcu/harbour-multi-sensor-tracking) -- mm-wave radar, stereo camera, AIS, GNSS fused with EKF + Hungarian association; simulated scenarios with MOTP-style gates and real Copenhagen harbour runs.

## How MAVMRF relates

| Capability | Literature / open baselines | MAVMRF today |
|------------|----------------------------|--------------|
| Multi-modal sensing | AIS, radar, EO/IR, sonar in surveys | Simulated sonar / acoustic / optical / magnetic |
| Optical detect + track | YOLO + DeepSORT / SORT-family common | YOLO optional; SORT-style tracks; sim detections by default |
| Association / fusion | Hungarian, EKF, feature-level fusion | IoU match + weighted fusion (heuristic) |
| Validation | MOTP/RMSE on sim + real fixtures | Seeded simulation gates (docs/benchmarks/) |
| Live / recorded feeds | Public datasets + harbour recordings | SensorAdapter + JSON file replay; AIS/radar adapters are extension points |

For the integration contract and planned AIS/radar replay path, see [ARCHITECTURE.md](ARCHITECTURE.md) and [marmf/interfaces/sensor_adapter.py](../marmf/interfaces/sensor_adapter.py).
