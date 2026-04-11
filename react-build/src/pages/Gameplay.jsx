function Gameplay() {
  return (
    <>
      {/* Hero Section */}
      <section className="hero py-5">
        <div className="container text-center">
          <h1 className="display-1 fw-bold mb-4">Gameplay</h1>
          <p className="lead mb-5">Master tower defense across 9 historical eras</p>
        </div>
      </section>

      {/* Gameplay Overview */}
      <section className="py-5">
        <div className="container">
          <h2 className="text-center mb-5">Gameplay Overview</h2>
          <div className="row">
            <div className="col-lg-8 mx-auto">
              <p className="mb-4">
                Sakartvelo Defenders combines classic tower defense mechanics with
                historical accuracy and blockchain rewards. Each of the 9 eras
                offers unique challenges, tower types, and enemy formations based
                on real historical battles.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Core Mechanics */}
      <section className="py-5 bg-light">
        <div className="container">
          <h2 className="text-center mb-5">Core Mechanics</h2>
          <div className="row g-4">
            <div className="col-md-4">
              <div className="feature-card p-4 h-100">
                <div className="text-center mb-3">
                  <i className="fas fa-chess-rook"></i>
                </div>
                <h4 className="mb-3 text-center">Tower Placement</h4>
                <p>
                  Strategic tower placement is key. Each era introduces new tower
                  types inspired by historical defenses - from ancient stone
                  fortifications to medieval watchtowers.
                </p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="feature-card p-4 h-100">
                <div className="text-center mb-3">
                  <i className="fas fa-coins"></i>
                </div>
                <h4 className="mb-3 text-center">Resource Management</h4>
                <p>
                  Manage gold, food, and special resources unique to each era.
                  Every decision impacts your ability to defend against waves of
                  historically accurate enemies.
                </p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="feature-card p-4 h-100">
                <div className="text-center mb-3">
                  <i className="fas fa-scroll"></i>
                </div>
                <h4 className="mb-3 text-center">Historical Accuracy</h4>
                <p>
                  Battles are based on real historical events. Enemy formations,
                  weapons, and strategies reflect actual military tactics used in
                  Georgian history.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Era Progression */}
      <section className="py-5">
        <div className="container">
          <h2 className="text-center mb-5">Era Progression System</h2>
          <div className="row">
            <div className="col-lg-8 mx-auto">
              <p className="mb-4">
                Each era contains 20 levels with increasing difficulty. As you
                progress through the eras, you unlock new tower types, abilities,
                and historical knowledge. The difficulty curve is designed to be
                accessible to newcomers while challenging veteran players.
              </p>
              <ul className="list-group mb-4">
                <li className="list-group-item">
                  <strong>Era 1-3:</strong> Learn the basics with ancient and medieval defenses
                </li>
                <li className="list-group-item">
                  <strong>Era 4-6:</strong> Master advanced mechanics with Renaissance and Imperial warfare
                </li>
                <li className="list-group-item">
                  <strong>Era 7-9:</strong> Face the ultimate challenge with modern military strategies
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Tower Types */}
      <section className="py-5 bg-light">
        <div className="container">
          <h2 className="text-center mb-5">Tower Types</h2>
          <div className="row g-4">
            <div className="col-md-3">
              <div className="feature-card p-4 h-100 text-center">
                <i className="fas fa-archway mb-3"></i>
                <h5>Stone Towers</h5>
                <p>Basic defense towers with reliable damage output.</p>
              </div>
            </div>
            <div className="col-md-3">
              <div className="feature-card p-4 h-100 text-center">
                <i className="fas fa-bolt mb-3"></i>
                <h5>Lightning Towers</h5>
                <p>Fast-attack towers that chain damage to multiple enemies.</p>
              </div>
            </div>
            <div className="col-md-3">
              <div className="feature-card p-4 h-100 text-center">
                <i className="fas fa-fire mb-3"></i>
                <h5>Fire Towers</h5>
                <p>Area-of-effect damage towers perfect for crowd control.</p>
              </div>
            </div>
            <div className="col-md-3">
              <div className="feature-card p-4 h-100 text-center">
                <i className="fas fa-shield-halved mb-3"></i>
                <h5>Shield Towers</h5>
                <p>Support towers that slow enemies and boost nearby towers.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Blockchain Rewards */}
      <section className="py-5">
        <div className="container">
          <h2 className="text-center mb-5">Blockchain Rewards (SAKART)</h2>
          <div className="row">
            <div className="col-lg-8 mx-auto">
              <p className="mb-4">
                Players earn SAKART tokens through skilled gameplay - not through
                purchases. The blockchain integration is invisible to new players,
                with no wallet required to start playing. Advanced players can
                optionally connect wallets to trade and stake tokens.
              </p>
              <div className="row g-3">
                <div className="col-md-6">
                  <div className="feature-card p-3 h-100">
                    <h5>Free-to-Play First</h5>
                    <p>
                      Complete the entire game without ever touching blockchain
                      features. No wallet required.
                    </p>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="feature-card p-3 h-100">
                    <h5>Skill-Based Rewards</h5>
                    <p>
                      Earn SAKART by completing levels, achieving high scores, and
                      mastering historical challenges.
                    </p>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="feature-card p-3 h-100">
                    <h5>Transparent Economy</h5>
                    <p>
                      1.8% transaction fee funds development and community rewards.
                      All token flows are publicly auditable.
                    </p>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="feature-card p-3 h-100">
                    <h5>Zero Friction</h5>
                    <p>
                      No seed phrases, no gas fees, no crypto knowledge needed.
                      Blockchain is an invisible backend layer.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  )
}

export default Gameplay
