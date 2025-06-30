from genmo.mochi_preview.pipelines import (
    DecoderModelFactory,
    DitModelFactory,
    MochiMultiGPUPipeline,
    T5ModelFactory,
    linear_quadratic_schedule,
)

class Inference:
    def __init__(self):
        pass

def load_model():
    global num_gpus, pipeline, model_dir_path, lora_path
    if pipeline is None:
        MOCHI_DIR = model_dir_path
        print(f"Launching with {num_gpus} GPUs. If you want to force single GPU mode use CUDA_VISIBLE_DEVICES=0.")
        klass = MochiMultiGPUPipeline
        kwargs = dict(
            text_encoder_factory=T5ModelFactory(),
            dit_factory=DitModelFactory(
                model_path=f"{MOCHI_DIR}/dit.safetensors",
                lora_path=lora_path,
                model_dtype="bf16",
            ),
            decoder_factory=DecoderModelFactory(
                model_path=f"{MOCHI_DIR}/decoder.safetensors",
            ),
        )
        if num_gpus > 1:
            assert not lora_path, f"Lora not supported in multi-GPU mode"
            assert not cpu_offload, "CPU offload not supported in multi-GPU mode"
            kwargs["world_size"] = num_gpus
        else:
            kwargs["cpu_offload"] = cpu_offload
            kwargs["decode_type"] = "tiled_spatial"
            kwargs["fast_init"] = not lora_path
            kwargs["strict_load"] = not lora_path
            kwargs["decode_args"] = dict(overlap=8)
        pipeline = klass(**kwargs)