function Home() {
  return (
    <>
      {/* Hero Section */}
      <section className="hero py-5">
        <div className="container text-center">
          <h1 className="display-1 fw-bold mb-4">Sakartvelo Defenders</h1>
          <p className="lead mb-5">
            The world&apos;s first tower defense game rooted in 9 historical eras of
            Georgian culture, with blockchain integration
          </p>
          <a href="#features" className="btn btn-lg cta-button px-5 py-3 fw-bold">
            Discover History
          </a>
        </div>
      </section>

      {/* Key Features */}
      <section id="features" className="py-5">
        <div className="container">
          <h2 className="text-center mb-5">Why Sakartvelo Defenders Stands Apart</h2>
          <div className="row g-4">
            <div className="col-md-4">
              <div className="feature-card p-4 h-100">
                <div className="text-center mb-3">
                  <i className="fas fa-flag"></i>
                </div>
                <h4 className="mb-3 text-center">Authentic Cultural Depth</h4>
                <p>
                  Each era (1,500 BC - present) features historically accurate
                  battles, enemies, and mechanics. No &apos;culture as
                  skin&apos; - history drives gameplay itself.
                </p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="feature-card p-4 h-100">
                <div className="text-center mb-3">
                  <i className="fas fa-cash-stack"></i>
                </div>
                <h4 className="mb-3 text-center">Blockchain Done Right</h4>
                <p>
                  Zero wallet friction, skill-based SAKART rewards, and 1.8%
                  transparent fee. No pay-to-win, no seed phrases.
                </p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="feature-card p-4 h-100">
                <div className="text-center mb-3">
                  <i className="fas fa-person-workspace"></i>
                </div>
                <h4 className="mb-3 text-center">Solo-Dev Sustainable</h4>
                <p>
                  Built for $100/month hosting with no servers. Game state stored
                  off-chain, blockchain only for tokens.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Historical Eras */}
      <section className="py-5 bg-light">
        <div className="container">
          <h2 className="text-center mb-5">Nine Historical Eras of Georgia</h2>
          <div className="row g-4">
            <div className="col-md-4">
              <div className="feature-card p-4 h-100">
                <h4 className="text-center mb-3">1. Mtskheta Period (1500 BC - 337 AD)</h4>
                <p>
                  Early Georgian kingdoms, including the legendary city of
                  Mtskheta and early Christian influences.
                </p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="feature-card p-4 h-100">
                <h4 className="text-center mb-3">2. Kingdom of Iberia (337 - 888 AD)</h4>
                <p>
                  Christianization period, including the legendary Queen
                  Tamar&apos;s reign and the development of Georgian culture.
                </p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="feature-card p-4 h-100">
                <h4 className="text-center mb-3">3. Medieval Kingdoms (888 - 1466)</h4>
                <p>
                  Golden age of Georgian art, literature, and architecture with
                  the development of the Georgian Orthodox Church.
                </p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="feature-card p-4 h-100">
                <h4 className="text-center mb-3">4. Georgian Principality (1466 - 1502)</h4>
                <p>
                  Period of division and conflict, leading to eventual
                  unification.
                </p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="feature-card p-4 h-100">
                <h4 className="text-center mb-3">5. Kingdom of Kartli (1502 - 1614)</h4>
                <p>
                  Reconstruction and renaissance period under the rule of the
                  Bagrationi dynasty.
                </p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="feature-card p-4 h-100">
                <h4 className="text-center mb-3">6. Russian Period (1614 - 1801)</h4>
                <p>
                  Influence of Russian rule and cultural integration with the
                  broader European trends.
                </p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="feature-card p-4 h-100">
                <h4 className="text-center mb-3">7. Russian Empire (1801 - 1917)</h4>
                <p>Period of Russian control and gradual loss of autonomy.</p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="feature-card p-4 h-100">
                <h4 className="text-center mb-3">8. Democratic Period (1918 - 1921)</h4>
                <p>
                  Moment of independence, with the rise of the Georgian
                  Democratic Republic.
                </p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="feature-card p-4 h-100">
                <h4 className="text-center mb-3">9. Soviet Period (1921 - 1991)</h4>
                <p>
                  Integration into the Soviet Union and eventual independence in
                  1991.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-5 bg-light">
        <div className="container text-center">
          <h2 className="mb-4">Join Our Early Access</h2>
          <p className="mb-4">
            Get notified when the first 3 eras (60 levels) launch. No spam, just
            updates on historical gameplay.
          </p>
          <form
            className="d-flex justify-content-center mb-4"
            action="#"
            onSubmit={(e) => e.preventDefault()}
          >
            <input
              type="email"
              className="form-control me-2"
              placeholder="Your email address"
              style={{ maxWidth: 350 }}
            />
            <button type="submit" className="btn cta-button px-4">
              Join Waitlist
            </button>
          </form>
          <small className="text-muted">
            We&apos;ll never share your email. All updates about historical gameplay
            mechanics will be sent here.
          </small>
        </div>
      </section>
    </>
  )
}

export default Home
