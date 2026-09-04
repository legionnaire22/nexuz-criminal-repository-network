import React, { useEffect, useRef, useState } from 'react';
import cytoscape from 'cytoscape';

// Exported so App.jsx can call it after reset/disruption layout runs
export function revealEdgesSequentially(cy, speed = 1.0) {
  const edges = cy.edges().toArray();
  if (edges.length === 0) return;

  const priority = (e) => {
    const srcType = e.source().data('type');
    const tgtType = e.target().data('type');
    if (srcType === 'target' || tgtType === 'target') return 2;  // last — the climax
    if (srcType === 'broker' || tgtType === 'broker') return 1;  // second
    return 0;                                                      // noise edges first
  };

  edges.sort((a, b) => priority(a) - priority(b));

  // Hide all edges immediately
  cy.edges().style({ opacity: 0, width: 0 });

  // Calculate dynamic interval based on number of edges and speed
  const stepDelay = Math.max(15, Math.min(80, Math.round(1800 / edges.length / Math.max(0.2, speed))));

  // Staggered reveal
  edges.forEach((edge, i) => {
    setTimeout(() => {
      const isRaw = edge.hasClass('raw-mode');
      const targetOpacity = isRaw ? 0.35 : 0.7;
      const targetWidth = isRaw ? 1.2 : (edge.data('weight') || 2);
      edge.animate({
        style: { opacity: targetOpacity, width: targetWidth },
        duration: Math.max(100, Math.round(300 / Math.max(0.2, speed))),
        easing: 'ease-in-out-cubic'
      });
    }, i * stepDelay);
  });
}

export function GraphCanvas({
  currentCase,
  topology,
  isHypothesisRunning,
  isDisrupted,
  isAnalyzed,
  hypothesisStatus,
  hypothesisBanner,
  playbackSpeed,
  onRunHypothesis,
  onToggleDisruption,
  onResetGraph,
  onSpeedChange,
  onSelectSuspect,
  suspects,
  cyInstanceRef
}) {
  const cyRef = useRef(null);
  const [hoveredEntity, setHoveredEntity] = useState(null);
  const isAnalyzedRef = useRef(isAnalyzed);
  isAnalyzedRef.current = isAnalyzed;

  useEffect(() => {
    if (!cyRef.current) return;

    const cy = cytoscape({
      container: cyRef.current,
      style: [
        {
          selector: 'node',
          style: {
            'shape': 'ellipse',
            'label': 'data(icon)',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size': '15px',
            'font-family': 'Apple Color Emoji, Segoe UI Emoji, Noto Color Emoji, sans-serif',
            'color': '#ffffff',
            'background-color': '#0f172a',
            'background-opacity': 0.28,
            'width': 32,
            'height': 32,
            'border-width': 1.5,
            'border-color': '#334155',
            'border-opacity': 0.85,
            'opacity': 0.65,
            'transition-property': 'background-color, border-color, width, height, opacity, shadow-blur',
            'transition-duration': '0.35s'
          }
        },
        {
          selector: 'node[type = "target"]',
          style: {
            'shape': 'ellipse',
            'label': 'data(icon)',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size': '18px',
            'background-color': '#ff2a55',
            'background-opacity': 0.28,
            'border-color': '#ff2a55',
            'border-width': 3,
            'shadow-blur': 36,
            'shadow-color': '#ff2a55',
            'shadow-opacity': 0.95,
            'width': 40,
            'height': 40,
            'opacity': 1.0,
            'z-index': 100
          }
        },
        {
          selector: 'node[type = "broker"]',
          style: {
            'shape': 'ellipse',
            'label': 'data(icon)',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size': '17px',
            'background-color': '#a855f7',
            'background-opacity': 0.28,
            'border-color': '#c084fc',
            'border-width': 3,
            'shadow-blur': 30,
            'shadow-color': '#a855f7',
            'shadow-opacity': 0.9,
            'width': 36,
            'height': 36,
            'opacity': 1.0,
            'z-index': 90
          }
        },
        {
          selector: 'node[type = "phone"]',
          style: {
            'shape': 'ellipse',
            'label': 'data(icon)',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size': '16px',
            'background-color': '#0284c7',
            'background-opacity': 0.28,
            'border-color': '#38bdf8',
            'border-width': 2.5,
            'shadow-blur': 22,
            'shadow-color': '#0284c7',
            'shadow-opacity': 0.85,
            'width': 32,
            'height': 32,
            'opacity': 1.0,
            'z-index': 85
          }
        },
        {
          selector: 'node[type = "vehicle"]',
          style: {
            'shape': 'ellipse',
            'label': 'data(icon)',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size': '16px',
            'background-color': '#d97706',
            'background-opacity': 0.28,
            'border-color': '#fbbf24',
            'border-width': 2.5,
            'shadow-blur': 22,
            'shadow-color': '#f59e0b',
            'shadow-opacity': 0.85,
            'width': 32,
            'height': 32,
            'opacity': 1.0,
            'z-index': 85
          }
        },
        {
          selector: 'node[type = "account"]',
          style: {
            'shape': 'ellipse',
            'label': 'data(icon)',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size': '16px',
            'background-color': '#059669',
            'background-opacity': 0.28,
            'border-color': '#34d399',
            'border-width': 2.5,
            'shadow-blur': 22,
            'shadow-color': '#10b981',
            'shadow-opacity': 0.85,
            'width': 32,
            'height': 32,
            'opacity': 1.0,
            'z-index': 85
          }
        },
        {
          selector: 'node[type = "organization"]',
          style: {
            'shape': 'ellipse',
            'label': 'data(icon)',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size': '16px',
            'background-color': '#e11d48',
            'background-opacity': 0.28,
            'border-color': '#fda4af',
            'border-width': 2.5,
            'shadow-blur': 22,
            'shadow-color': '#f43f5e',
            'shadow-opacity': 0.85,
            'width': 34,
            'height': 34,
            'opacity': 1.0,
            'z-index': 85
          }
        },
        {
          selector: 'node[type = "tower"], node[type = "location"]',
          style: {
            'shape': 'ellipse',
            'label': 'data(icon)',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size': '15px',
            'background-color': '#0d9488',
            'background-opacity': 0.28,
            'border-color': '#2dd4bf',
            'border-width': 2,
            'shadow-blur': 18,
            'shadow-color': '#14b8a6',
            'shadow-opacity': 0.75,
            'width': 30,
            'height': 30,
            'opacity': 0.95,
            'z-index': 80
          }
        },
        {
          selector: 'node[type = "cleared"]',
          style: {
            'shape': 'ellipse',
            'label': 'data(icon)',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size': '15px',
            'background-color': '#00ff88',
            'background-opacity': 0.25,
            'border-color': '#86efac',
            'border-width': 2,
            'shadow-blur': 16,
            'shadow-color': '#00ff88',
            'shadow-opacity': 0.7,
            'width': 28,
            'height': 28,
            'opacity': 0.85,
            'z-index': 50
          }
        },
        {
          selector: 'node[type = "noise"]',
          style: {
            'shape': 'ellipse',
            'label': 'data(icon)',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size': '12px',
            'background-color': '#0f172a',
            'background-opacity': 0.25,
            'border-color': '#1e293b',
            'border-width': 1,
            'width': 22,
            'height': 22,
            'opacity': 0.55,
            'shadow-blur': 0,
            'z-index': 1
          }
        },
        {
          selector: 'node[type = "arrested"]',
          style: {
            'background-color': '#334155',
            'background-opacity': 0.4,
            'border-color': '#ff2a55',
            'border-width': 4,
            'border-style': 'dashed',
            'color': '#ff2a55'
          }
        },
        {
          selector: 'node:selected',
          style: {
            'border-color': '#00f0ff',
            'border-width': 4,
            'shadow-blur': 28,
            'shadow-color': '#00f0ff',
            'shadow-opacity': 1,
            'opacity': 1.0
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 1.0,
            'line-color': '#0e1726',
            'target-arrow-color': '#0e1726',
            'target-arrow-shape': 'none',
            'curve-style': 'bezier',
            'opacity': 0.08,
            'arrow-scale': 0.8,
            'transition-property': 'line-color, opacity, width',
            'transition-duration': '0.4s'
          }
        },
        {
          selector: 'edge[color = "#475569"]',
          style: {
            'line-color': '#080d17',
            'width': 0.6,
            'opacity': 0.04,
            'target-arrow-shape': 'none',
            'z-index': 1
          }
        },
        {
          selector: 'edge[color = "#ff2a55"], edge[color = "#ffb800"], edge[color = "#a855f7"]',
          style: {
            'width': 4.5,
            'line-color': 'data(color)',
            'target-arrow-color': 'data(color)',
            'target-arrow-shape': 'triangle',
            'arrow-scale': 1.15,
            'opacity': 1.0,
            'z-index': 80
          }
        },
        {
          selector: 'edge[status = "probe-fail"]',
          style: {
            'line-color': '#ff2a55',
            'line-style': 'dashed',
            'width': 3,
            'opacity': 0.95,
            'z-index': 95
          }
        },
        {
          selector: 'edge[status = "severed"]',
          style: {
            'line-color': '#475569',
            'line-style': 'dotted',
            'opacity': 0.2
          }
        },
        {
          selector: 'edge:hover',
          style: {
            'width': 4,
            'opacity': 1.0,
            'line-color': '#00f0ff',
            'target-arrow-color': '#00f0ff',
            'target-arrow-shape': 'triangle'
          }
        },
        {
          selector: 'node.raw-mode',
          style: {
            'shape': 'ellipse',
            'label': 'data(icon)',
            'text-valign': 'center',
            'text-halign': 'center',
            'background-color': '#0f172a',
            'background-opacity': 0.35,
            'border-color': '#334155',
            'border-width': 1.5,
            'border-opacity': 0.85,
            'width': 28,
            'height': 28,
            'color': '#ffffff',
            'font-size': '14px',
            'shadow-blur': 0,
            'opacity': 0.85
          }
        },
        {
          selector: 'edge.raw-mode',
          style: {
            'line-color': '#334155',
            'width': 1.2,
            'opacity': 0.35,
            'target-arrow-shape': 'none'
          }
        }
      ],
      layout: { name: 'cose', animate: false }
    });

    const showTooltip = (isNode, target, evt) => {
      const rect = cyRef.current ? cyRef.current.getBoundingClientRect() : { width: 600, height: 500 };
      const pos = evt.renderedPosition || { x: 200, y: 200 };
      const analyzed = isAnalyzedRef.current;

      if (isNode) {
        const nodeType = target.data('type');
        const displayType = !analyzed 
          ? 'Raw Ingested Record (Pending Analysis)' 
          : nodeType === 'target' 
            ? 'Prime Suspect (Human Accused)' 
            : nodeType === 'broker' 
              ? 'Covert Bridge / Facilitator' 
              : nodeType === 'vehicle'
                ? 'Seized Transport Asset (Vehicle)'
                : nodeType === 'account'
                  ? 'Flagged Mule Account (Banking)'
                  : nodeType === 'organization'
                    ? 'Corporate Shell Conduit (Entity)'
                    : nodeType === 'phone'
                      ? 'Monitored Telecom Endpoint (SIM)'
                      : (nodeType === 'tower' || nodeType === 'location')
                        ? 'Cellular BTS Location Tower'
                        : nodeType === 'cleared' 
                          ? 'Cleared Citizen / Witness' 
                          : nodeType === 'noise' 
                            ? 'Ambient Signal Noise' 
                            : 'Corroborated Forensic Node';

        const badgeClass = !analyzed
          ? 'score-pending'
          : nodeType === 'target'
            ? 'score-critical'
            : (nodeType === 'broker' || nodeType === 'vehicle' || nodeType === 'account' || nodeType === 'organization')
              ? 'score-warning'
              : nodeType === 'cleared'
                ? 'score-cleared'
                : 'score-analyzed';

        setHoveredEntity({
          isNode: true,
          title: target.data('label') || target.id(),
          type: displayType,
          badgeClass: badgeClass,
          reason: target.data('reason') || 'Canonical entity record participating in investigation.',
          doc: target.data('doc') || 'fir_sandstorm_1.txt',
          metric: !analyzed ? 'Awaiting Pipeline Scan' : (target.data('metric') || 'Verified Forensic Hub'),
          x: Math.min(Math.max(15, pos.x + 18), rect.width - 330),
          y: Math.min(Math.max(65, pos.y - 40), rect.height - 190)
        });
      } else {
        const src = target.source().data('label') || target.data('source');
        const tgt = target.target().data('label') || target.data('target');
        const edgeRel = target.data('rel_type') || 'CONNECTED';
        const edgeColor = target.data('color');

        const displayType = !analyzed
          ? 'Raw Signal Link (Pending Analysis)'
          : edgeRel;

        const badgeClass = !analyzed
          ? 'score-pending'
          : edgeColor === '#ff2a55'
            ? 'score-critical'
            : (edgeColor === '#ffb800' || edgeColor === '#a855f7')
              ? 'score-warning'
              : 'score-analyzed';

        setHoveredEntity({
          isNode: false,
          title: `${edgeRel}: ${src} → ${tgt}`,
          type: displayType,
          badgeClass: badgeClass,
          reason: target.data('reason') || 'Forensic financial/telecom connection between nodes.',
          doc: target.data('doc') || 'txn_sandstorm.csv',
          metric: !analyzed ? 'Awaiting Pipeline Scan' : (target.data('metric') || 'Verified Forensic Edge'),
          x: Math.min(Math.max(15, pos.x + 18), rect.width - 330),
          y: Math.min(Math.max(65, pos.y - 40), rect.height - 190)
        });
      }
    };

    cy.on('mouseover', 'node', (evt) => showTooltip(true, evt.target, evt));
    cy.on('tap', 'node', (evt) => {
      showTooltip(true, evt.target, evt);
      const node = evt.target;
      const match = suspects.find(s => s.id === node.id() || s.name.toLowerCase() === (node.data('label') || '').toLowerCase());
      if (match) onSelectSuspect(match);
    });
    cy.on('mouseout', 'node', () => setHoveredEntity(null));

    cy.on('mouseover', 'edge', (evt) => showTooltip(false, evt.target, evt));
    cy.on('tap', 'edge', (evt) => showTooltip(false, evt.target, evt));
    cy.on('mouseout', 'edge', () => setHoveredEntity(null));
    cy.on('tap', (evt) => { if (evt.target === cy) setHoveredEntity(null); });

    cyInstanceRef.current = cy;

    // Load initial elements
    cy.elements().remove();
    cy.add(topology);

    // If not analyzed, apply uniform raw appearance
    if (!isAnalyzed) {
      cy.elements().addClass('raw-mode');
    }

    const layout = cy.layout({
      name: 'cose',
      animate: true,
      animationDuration: 750,
      nodeRepulsion: 7500,
      idealEdgeLength: 90,
      padding: 30
    });

    // Sequential edge reveal after layout finishes
    layout.on('layoutstop', () => {
      revealEdgesSequentially(cy, playbackSpeed);
    });

    layout.run();

    return () => cy.destroy();
  }, [currentCase]);

  // Synchronize raw-mode and prune insignificant noise arrows when isAnalyzed toggles
  useEffect(() => {
    const cy = cyInstanceRef.current;
    if (!cy) return;
    if (isAnalyzed) {
      cy.elements().removeClass('raw-mode');

      // 1. Completely prune & hide all insignificant noise nodes
      const noiseNodes = cy.nodes().filter(n => n.data('type') === 'noise' || n.id().startsWith('N'));
      noiseNodes.style({
        'opacity': 0,
        'width': 0,
        'height': 0,
        'label': '',
        'border-width': 0,
        'display': 'none'
      });

      // 2. Completely remove all arrows and edges pointing to insignificant/civilian noise nodes
      const noiseEdges = cy.edges().filter(e => {
        const sType = e.source().data('type');
        const tType = e.target().data('type');
        const sId = e.source().id();
        const tId = e.target().id();
        return sType === 'noise' || tType === 'noise' || sId.startsWith('N') || tId.startsWith('N') || e.data('color') === '#475569';
      });
      noiseEdges.style({
        'opacity': 0,
        'width': 0,
        'target-arrow-shape': 'none',
        'display': 'none'
      });

      // 3. Highlight core syndicate crime nodes with neon glow
      const crimeNodes = cy.nodes().filter(n => n.data('type') === 'target' || n.data('type') === 'broker');
      crimeNodes.style({
        'opacity': 1.0,
        'border-width': 3.5,
        'shadow-blur': 42,
        'shadow-opacity': 1
      });

      // 4. Highlight verified syndicate crime edges with prominent arrows
      const crimeEdges = cy.edges().difference(noiseEdges);
      crimeEdges.style({
        'opacity': 1.0,
        'width': 4.0,
        'target-arrow-shape': 'triangle',
        'target-arrow-color': e => e.data('color') || '#00f0ff',
        'line-color': e => e.data('color') || '#00f0ff',
        'display': 'element'
      });
    } else {
      cy.elements().addClass('raw-mode');
      cy.elements().removeStyle();
    }
  }, [isAnalyzed]);

  return (
    <section className="tactical-panel graph-panel-wrap">
      {/* Formation & Disruption Controls Toolbar */}
      <div className="canvas-hud-toolbar">
        <div className="animation-playback-bar">
          <button
            className={`btn-anim-ctrl btn-investigate-pulse ${isHypothesisRunning ? 'active' : ''}`}
            onClick={onRunHypothesis}
            disabled={isHypothesisRunning}
            title="Trigger Multi-Agent AI Investigation: Scan Anomaly Patterns, Score Risk, Reveal Syndicate & Stream Debate"
          >
            <i className={`fa-solid ${isHypothesisRunning ? 'fa-spinner fa-spin' : isAnalyzed ? 'fa-rotate' : 'fa-play'}`} style={{ color: isAnalyzed ? 'var(--cyan-bright)' : '#00ff88' }}></i>
            <span>{isHypothesisRunning ? 'Investigating...' : isAnalyzed ? 'Re-run Investigation' : 'Run AI Investigation'}</span>
          </button>

          <button
            className="btn-anim-ctrl"
            onClick={onResetGraph}
            title="Reset Graph to Raw Ingested State"
          >
            <i className="fa-solid fa-rotate"></i>
            <span>Reset</span>
          </button>

          {/* Speed slider */}
          <div className="speed-slider-wrap">
            <i className="fa-solid fa-gauge-high" style={{ color: 'var(--cyan-bright)' }}></i>
            <span>Speed:</span>
            <input
              type="range"
              min="0.2"
              max="4.0"
              step="0.1"
              value={playbackSpeed}
              onChange={(e) => onSpeedChange(parseFloat(e.target.value))}
              className="speed-slider"
              title="Adjust Investigation Velocity (0.2x to 4.0x)"
            />
            <span style={{ color: 'var(--cyan-bright)', fontWeight: 'bold', minWidth: '32px' }}>
              {playbackSpeed.toFixed(1)}x
            </span>
          </div>
        </div>

        {/* Status pill — only visible while hypothesis is running */}
        {isHypothesisRunning && (
          <div className="formation-status-pill">
            <div className="pulse-radar-dot"></div>
            <span>{hypothesisStatus}</span>
          </div>
        )}
      </div>

      {/* Cytoscape Container */}
      <div id="cy" ref={cyRef}></div>

      {/* Interactive Hover Tooltip for Forensic Reasoning */}
      {hoveredEntity && (
        <div 
          className="forensic-hover-card" 
          style={{ top: `${hoveredEntity.y}px`, left: `${hoveredEntity.x}px` }}
        >
          <div className="forensic-hover-head">
            <span className="forensic-title">{hoveredEntity.title}</span>
            <span className={`forensic-badge ${hoveredEntity.badgeClass}`}>
              {hoveredEntity.type}
            </span>
          </div>
          
          <div style={{ fontSize: '0.62rem', color: 'var(--cyan-bright)', fontFamily: 'var(--font-mono)', marginBottom: '3px' }}>
            FORENSIC REASON FOR EXISTENCE:
          </div>
          <div className="forensic-reason-box">
            {hoveredEntity.reason}
          </div>

          <div className="forensic-metadata-row">
            <span><i className="fa-solid fa-file-lines"></i> Source: {hoveredEntity.doc}</span>
            <span>{hoveredEntity.metric}</span>
          </div>
        </div>
      )}

      {/* Bottom Canvas Legend */}
      <div className="graph-legend-overlay">
        {!isAnalyzed ? (
          <div className="legend-item">
            <span className="legend-dot" style={{ background: '#475569' }}></span> Raw Ingested Records (Click 'Run AI Investigation' to scan)
          </div>
        ) : (
          <>
            <div className="legend-item"><span className="legend-dot" style={{ background: '#ff2a55' }}></span> Prime Suspect</div>
            <div className="legend-item"><span className="legend-dot" style={{ background: '#a855f7' }}></span> Covert Bridge</div>
            <div className="legend-item"><span className="legend-dot" style={{ background: '#0284c7' }}></span> 📱 Monitored Phone</div>
            <div className="legend-item"><span className="legend-dot" style={{ background: '#d97706' }}></span> 🚐 Seized Asset / Mule</div>
            <div className="legend-item"><span className="legend-dot" style={{ background: '#00ff88' }}></span> Cleared Citizen</div>
          </>
        )}
      </div>
    </section>
  );
}
