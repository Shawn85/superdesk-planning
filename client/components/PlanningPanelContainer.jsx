import React from 'react'
import { connect } from 'react-redux'
import * as actions from '../actions'
import { SelectAgenda, PlanningItem } from './index'
import * as selectors from '../selectors'

class PlanningPanel extends React.Component {

    constructor(props) {
        super(props)
    }

    componentDidMount() {
        this.props.fetchAgendas()
    }

    render() {
        const {
            openCreateAgenda,
            planningList,
            openPlanningEditor,
            currentAgenda,
            planningsAreLoading
        } = this.props
        return (
            <div className="Planning__planning">
                <div className="subnav">
                    <h3 className="subnav__page-title">
                        <span>
                            <span>Planning</span>
                        </span>
                    </h3>
                    <SelectAgenda />
                    <div className="subnav__button-stack--square-buttons">
                        <div className="refresh-box pull-right" />
                        <div className="navbtn" title="Create">
                            <button className="sd-create-btn"
                                    onClick={openCreateAgenda.bind(null, null)}>
                                <i className="svg-icon-plus" />
                                <span className="circle" />
                            </button>
                        </div>
                    </div>
                </div>
                <ul className="Planning__planning__list list-view compact-view">
                    {currentAgenda &&
                        <li
                            className="Planning__planning__add"
                            onClick={openPlanningEditor.bind(null, null)}>
                            <i className="svg-icon-plus" /> Create a planning
                        </li>
                    }
                    {(planningList && planningList.length > 0) && planningList.map((planning) => (
                        <PlanningItem
                            key={planning._id}
                            item={planning}
                            onClick={openPlanningEditor.bind(null, planning._id)} />
                    ))}
                </ul>
                {
                    planningsAreLoading &&
                        <div className="Planning__planning__empty-message">
                            Loading
                        </div>
                    || !currentAgenda &&
                        <div className="Planning__planning__empty-message">
                            There is no selected calendar.<br/>
                            Choose one in the above dropdown.
                        </div>
                    || (planningList && planningList.length < 1) &&
                        <div className="Planning__planning__empty-message">
                            There is no planning yet
                            {currentAgenda &&
                                <div>
                                    in the agenda&nbsp;
                                    <strong>{currentAgenda.name}</strong>.
                                </div>
                            }
                            <div>Drag and drop an event here to start a planning</div>
                        </div>
                }
            </div>
        )
    }
}

PlanningPanel.propTypes = {
    currentAgenda: React.PropTypes.object,
    fetchAgendas: React.PropTypes.func.isRequired,
    openCreateAgenda: React.PropTypes.func.isRequired,
    planningList: React.PropTypes.array.isRequired,
    planningsAreLoading: React.PropTypes.bool,
    openPlanningEditor: React.PropTypes.func.isRequired,
}

const mapStateToProps = (state) => ({
    currentAgenda: selectors.getCurrentAgenda(state),
    planningList: selectors.getCurrentAgendaPlannings(state),
    planningsAreLoading: state.planning.planningsAreLoading
})

const mapDispatchToProps = (dispatch) => ({
    openCreateAgenda: () => dispatch(actions.showModal({ modalType: 'CREATE_AGENDA' })),
    fetchAgendas: () => dispatch(actions.fetchAgendas()),
    openPlanningEditor: (planning) => (dispatch(actions.openPlanningEditor(planning)))
})

export const PlanningPanelContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(PlanningPanel)