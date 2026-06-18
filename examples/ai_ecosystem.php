<?php

declare(strict_types=1);

/**
 * Comprehensive AI Ecosystem - execution-ready CLI example.
 *
 * Usage:
 *   php examples/ai_ecosystem.php
 *   php examples/ai_ecosystem.php --format=json
 *   php examples/ai_ecosystem.php --help
 *   php examples/ai_ecosystem.php --validate
 */

error_reporting(E_ALL);
ini_set('display_errors', '1');

interface Describable
{
    public function describe(): string;
}

interface EcosystemComponent extends Describable
{
    public function name(): string;

    public function category(): string;

    /** @return list<string> */
    public function capabilities(): array;

    /** @return list<string> */
    public function dependencies(): array;

    /** @return list<string> */
    public function governanceConsiderations(): array;

    /** @return array{name: string, category: string, description: string, capabilities: list<string>, dependencies: list<string>, governance: list<string>} */
    public function toArray(): array;
}

abstract class AbstractAIComponent implements EcosystemComponent
{
    /**
     * @param list<string> $capabilities
     * @param list<string> $dependencies
     * @param list<string> $governanceConsiderations
     */
    public function __construct(
        private readonly string $name,
        private readonly string $category,
        private readonly string $description,
        private readonly array $capabilities,
        private readonly array $dependencies,
        private readonly array $governanceConsiderations,
    ) {
    }

    public function name(): string
    {
        return $this->name;
    }

    public function category(): string
    {
        return $this->category;
    }

    public function describe(): string
    {
        return sprintf('%s: %s', $this->name, $this->description);
    }

    public function capabilities(): array
    {
        return $this->capabilities;
    }

    public function dependencies(): array
    {
        return $this->dependencies;
    }

    public function governanceConsiderations(): array
    {
        return $this->governanceConsiderations;
    }

    public function toArray(): array
    {
        return [
            'name' => $this->name,
            'category' => $this->category,
            'description' => $this->description,
            'capabilities' => $this->capabilities,
            'dependencies' => $this->dependencies,
            'governance' => $this->governanceConsiderations,
        ];
    }
}

final class AIComponentFactory
{
    /** @var array<class-string<EcosystemComponent>, EcosystemComponent> */
    private static array $instances = [];

    /**
     * @param class-string<EcosystemComponent> $className
     */
    public static function get(string $className): EcosystemComponent
    {
        if (!class_exists($className)) {
            throw new InvalidArgumentException("Component class does not exist: {$className}");
        }

        if (!is_subclass_of($className, EcosystemComponent::class)) {
            throw new InvalidArgumentException("Component must implement EcosystemComponent: {$className}");
        }

        if (!isset(self::$instances[$className])) {
            self::$instances[$className] = new $className();
        }

        return self::$instances[$className];
    }
}

// Core AI Technologies.
final class TransformerArchitecture extends AbstractAIComponent
{
    public function __construct()
    {
        parent::__construct(
            'Transformer Architecture',
            'Core AI Technologies',
            'Attention-based foundation for modern language, vision, speech, and multimodal systems.',
            ['self-attention', 'sequence modeling', 'multimodal representation learning'],
            ['large datasets', 'accelerated compute', 'tokenization or embedding pipelines'],
            ['dataset provenance', 'bias evaluation', 'model transparency'],
        );
    }
}

final class MachineLearning extends AbstractAIComponent
{
    public function __construct()
    {
        parent::__construct(
            'Machine Learning',
            'Core AI Technologies',
            'Algorithms that learn statistical patterns from data to support prediction and decision workflows.',
            ['classification', 'regression', 'ranking', 'forecasting'],
            ['quality data', 'feature engineering', 'evaluation metrics'],
            ['overfitting control', 'data privacy', 'human review for critical decisions'],
        );
    }
}

final class DeepLearning extends AbstractAIComponent
{
    public function __construct()
    {
        parent::__construct(
            'Deep Learning',
            'Core AI Technologies',
            'Multi-layer neural networks for extracting complex patterns from unstructured and structured data.',
            ['representation learning', 'image recognition', 'speech recognition', 'generative modeling'],
            ['GPUs or TPUs', 'training data', 'model monitoring'],
            ['explainability', 'energy usage', 'robustness testing'],
        );
    }
}

final class NaturalLanguageProcessing extends AbstractAIComponent
{
    public function __construct()
    {
        parent::__construct(
            'Natural Language Processing',
            'Core AI Technologies',
            'AI capabilities for understanding, generating, retrieving, and transforming human language.',
            ['summarization', 'question answering', 'translation', 'semantic search'],
            ['language models', 'corpora', 'retrieval systems'],
            ['hallucination mitigation', 'content safety', 'locale and accessibility coverage'],
        );
    }
}

final class ComputerVision extends AbstractAIComponent
{
    public function __construct()
    {
        parent::__construct(
            'Computer Vision',
            'Core AI Technologies',
            'AI methods for interpreting images, video, documents, and spatial signals.',
            ['object detection', 'segmentation', 'OCR', 'visual inspection'],
            ['annotated images', 'camera or document pipelines', 'edge or cloud inference'],
            ['surveillance risk', 'consent', 'domain-specific validation'],
        );
    }
}

// Infrastructure Components.
final class CloudComputing extends AbstractAIComponent
{
    public function __construct()
    {
        parent::__construct(
            'Cloud Computing',
            'Infrastructure',
            'Elastic compute, networking, and managed services for building and operating AI systems.',
            ['autoscaling', 'managed orchestration', 'global deployment'],
            ['identity management', 'networking', 'cost controls'],
            ['regional compliance', 'resilience planning', 'vendor risk management'],
        );
    }
}

final class DataStorage extends AbstractAIComponent
{
    public function __construct()
    {
        parent::__construct(
            'Data Storage',
            'Infrastructure',
            'Databases, object stores, warehouses, vector stores, and catalogs for AI-ready data.',
            ['data retention', 'metadata management', 'semantic retrieval'],
            ['backup strategy', 'schema governance', 'access policies'],
            ['PII handling', 'data lineage', 'right-to-delete workflows'],
        );
    }
}

final class ProcessingPower extends AbstractAIComponent
{
    public function __construct()
    {
        parent::__construct(
            'Processing Power',
            'Infrastructure',
            'GPU, TPU, CPU, and accelerator resources for training, fine-tuning, and inference.',
            ['distributed training', 'batch inference', 'low-latency serving'],
            ['hardware scheduling', 'thermal capacity', 'observability'],
            ['capacity planning', 'carbon footprint', 'failure isolation'],
        );
    }
}

final class APIsMicroservices extends AbstractAIComponent
{
    public function __construct()
    {
        parent::__construct(
            'APIs & Microservices',
            'Infrastructure',
            'Service interfaces that expose AI capabilities safely to products and operations.',
            ['model serving', 'workflow automation', 'service composition'],
            ['authentication', 'rate limiting', 'versioning'],
            ['audit logs', 'abuse prevention', 'secure secret management'],
        );
    }
}

// Tools and Platforms.
final class TensorFlow extends AbstractAIComponent
{
    public function __construct()
    {
        parent::__construct(
            'TensorFlow',
            'Tools & Platforms',
            'Open-source machine learning platform for model development and production deployment.',
            ['model training', 'serving', 'mobile and edge deployment'],
            ['Python ecosystem', 'data pipelines', 'runtime compatibility'],
            ['dependency patching', 'model reproducibility', 'supply-chain review'],
        );
    }
}

final class PyTorch extends AbstractAIComponent
{
    public function __construct()
    {
        parent::__construct(
            'PyTorch',
            'Tools & Platforms',
            'Deep learning framework widely used for research, experimentation, and production AI.',
            ['dynamic computation graphs', 'distributed training', 'model export'],
            ['Python ecosystem', 'CUDA or accelerator stack', 'experiment tracking'],
            ['reproducibility', 'dependency hygiene', 'deployment validation'],
        );
    }
}

final class HuggingFace extends AbstractAIComponent
{
    public function __construct()
    {
        parent::__construct(
            'Hugging Face',
            'Tools & Platforms',
            'Ecosystem for models, datasets, tokenizers, evaluation, and AI application tooling.',
            ['model discovery', 'fine-tuning workflows', 'dataset sharing'],
            ['model cards', 'dataset licenses', 'runtime environment'],
            ['license compliance', 'model risk review', 'dataset quality checks'],
        );
    }
}

// Applications.
final class Healthcare extends AbstractAIComponent
{
    public function __construct()
    {
        parent::__construct(
            'Healthcare',
            'Applications',
            'AI-assisted workflows for diagnostics, triage, research, operations, and patient engagement.',
            ['clinical decision support', 'medical imaging assistance', 'documentation automation'],
            ['validated clinical data', 'expert oversight', 'regulated deployment process'],
            ['patient privacy', 'clinical validation', 'clear accountability'],
        );
    }
}

final class AutonomousVehicles extends AbstractAIComponent
{
    public function __construct()
    {
        parent::__construct(
            'Autonomous Vehicles',
            'Applications',
            'AI systems for perception, prediction, planning, and control in mobility contexts.',
            ['sensor fusion', 'path planning', 'driver assistance'],
            ['simulation', 'sensor hardware', 'real-time compute'],
            ['safety cases', 'incident reporting', 'geofenced limitations'],
        );
    }
}

final class Finance extends AbstractAIComponent
{
    public function __construct()
    {
        parent::__construct(
            'Finance',
            'Applications',
            'AI for risk modeling, fraud detection, financial operations, customer support, and analytics.',
            ['fraud detection', 'risk scoring', 'portfolio analytics', 'customer automation'],
            ['secure data feeds', 'audit trails', 'model monitoring'],
            ['regulatory compliance', 'fair lending controls', 'explainable decisions'],
        );
    }
}

/**
 * @return array<string, list<class-string<EcosystemComponent>>>
 */
function ecosystemCategories(): array
{
    return [
        'Core AI Technologies' => [
            TransformerArchitecture::class,
            MachineLearning::class,
            DeepLearning::class,
            NaturalLanguageProcessing::class,
            ComputerVision::class,
        ],
        'Infrastructure' => [
            CloudComputing::class,
            DataStorage::class,
            ProcessingPower::class,
            APIsMicroservices::class,
        ],
        'Tools & Platforms' => [
            TensorFlow::class,
            PyTorch::class,
            HuggingFace::class,
        ],
        'Applications' => [
            Healthcare::class,
            AutonomousVehicles::class,
            Finance::class,
        ],
    ];
}

function ecosystemAsArray(): array
{
    $ecosystem = [];

    foreach (ecosystemCategories() as $category => $components) {
        $ecosystem[$category] = array_map(
            static fn (string $component): array => AIComponentFactory::get($component)->toArray(),
            $components,
        );
    }

    return $ecosystem;
}

function renderText(array $ecosystem): string
{
    $output = "=== Comprehensive AI Ecosystem ===\n\n";

    foreach ($ecosystem as $category => $components) {
        $output .= "--- {$category} ---\n";

        foreach ($components as $component) {
            $output .= $component['name'] . ': ' . $component['description'] . "\n";
            $output .= '  Capabilities: ' . implode(', ', $component['capabilities']) . "\n";
            $output .= '  Dependencies: ' . implode(', ', $component['dependencies']) . "\n";
            $output .= '  Governance: ' . implode(', ', $component['governance']) . "\n";
        }

        $output .= "\n";
    }

    return $output;
}


/**
 * @param array<string, list<array{name: string, category: string, description: string, capabilities: list<string>, dependencies: list<string>, governance: list<string>}>> $ecosystem
 * @return array{categories: int, components: int, capabilities: int, dependencies: int, governance_notes: int, validation_errors: int}
 */
function ecosystemMetrics(array $ecosystem): array
{
    $metrics = [
        'categories' => count($ecosystem),
        'components' => 0,
        'capabilities' => 0,
        'dependencies' => 0,
        'governance_notes' => 0,
        'validation_errors' => 0,
    ];

    foreach ($ecosystem as $category => $components) {
        if ($components === []) {
            $metrics['validation_errors']++;
        }

        foreach ($components as $component) {
            $metrics['components']++;
            $metrics['capabilities'] += count($component['capabilities']);
            $metrics['dependencies'] += count($component['dependencies']);
            $metrics['governance_notes'] += count($component['governance']);

            if ($component['category'] !== $category) {
                $metrics['validation_errors']++;
            }

            foreach (['name', 'description'] as $requiredStringField) {
                if (trim((string) $component[$requiredStringField]) === '') {
                    $metrics['validation_errors']++;
                }
            }

            foreach (['capabilities', 'dependencies', 'governance'] as $requiredListField) {
                if ($component[$requiredListField] === []) {
                    $metrics['validation_errors']++;
                }
            }
        }
    }

    return $metrics;
}

function renderSummary(array $ecosystem): string
{
    $metrics = ecosystemMetrics($ecosystem);

    return implode("\n", [
        '=== AI Ecosystem Health Summary ===',
        'Categories: ' . $metrics['categories'],
        'Components: ' . $metrics['components'],
        'Capabilities: ' . $metrics['capabilities'],
        'Dependencies: ' . $metrics['dependencies'],
        'Governance notes: ' . $metrics['governance_notes'],
        'Validation errors: ' . $metrics['validation_errors'],
        'Exit code: ' . ($metrics['validation_errors'] === 0 ? '0' : '1'),
        '',
    ]);
}

function renderJson(array $ecosystem): string
{
    $json = json_encode(
        [
            'title' => 'Comprehensive AI Ecosystem',
            'status' => ecosystemMetrics($ecosystem),
            'categories' => $ecosystem,
        ],
        JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE,
    );

    if ($json === false) {
        throw new RuntimeException('Failed to encode ecosystem JSON: ' . json_last_error_msg());
    }

    return $json . "\n";
}

function usage(): string
{
    return <<<TEXT
Comprehensive AI Ecosystem

Usage:
  php examples/ai_ecosystem.php [--format=text|json|summary]
  php examples/ai_ecosystem.php --validate
  php examples/ai_ecosystem.php --help

Options:
  --format=text     Render a readable categorized report (default).
  --format=json     Render machine-readable JSON with health metrics.
  --format=summary  Render a compact health summary.
  --validate        Validate the ecosystem and exit with 0 only when error count is zero.
  --help            Show this help message.

TEXT;
}

/** @param list<string> $argv */
function main(array $argv): int
{
    $format = 'text';
    $validateOnly = false;
    $arguments = array_slice($argv, 1);

    for ($index = 0; $index < count($arguments); $index++) {
        $argument = $arguments[$index];

        if ($argument === '--help' || $argument === '-h') {
            echo usage();
            return 0;
        }

        if ($argument === '--validate') {
            $format = 'summary';
            $validateOnly = true;
            continue;
        }

        if ($argument === '--format') {
            $nextArgument = $arguments[$index + 1] ?? null;
            if ($nextArgument === null || str_starts_with($nextArgument, '--')) {
                fwrite(STDERR, "Missing value for --format\n\n" . usage());
                return 1;
            }

            $format = $nextArgument;
            $index++;
            continue;
        }

        if (str_starts_with($argument, '--format=')) {
            $format = substr($argument, strlen('--format='));
            continue;
        }

        fwrite(STDERR, "Unknown argument: {$argument}\n\n" . usage());
        return 1;
    }

    $ecosystem = ecosystemAsArray();

    if ($format === 'json') {
        echo renderJson($ecosystem);
        return 0;
    }

    if ($format === 'summary') {
        $metrics = ecosystemMetrics($ecosystem);
        echo renderSummary($ecosystem);
        return $validateOnly && $metrics['validation_errors'] > 0 ? 1 : 0;
    }

    if ($format === 'text') {
        echo renderText($ecosystem);
        return 0;
    }

    fwrite(STDERR, "Unsupported format: {$format}\n\n" . usage());
    return 1;
}

if (PHP_SAPI === 'cli' && realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) {
    exit(main($argv));
}
